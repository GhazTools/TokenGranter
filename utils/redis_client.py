"""
file_name = redis_client.py
Created On: 2024/07/04
Lasted Updated: 2024/07/04
Description: _FILL OUT HERE_
Edit Log:
2024/07/04
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from pickle import loads, dumps
from typing import List, Any
from enum import Enum

# THIRD PARTY LIBRARY IMPORTS
from redis import Redis, ConnectionPool

# LOCAL LIBRARY IMPORTS
from utils.environment import Environment, EnvironmentVariableKeys


class KeyExpiredError(Exception):
    """
    An exception class to raise when the key has expired.
    """

    def __init__(self, key, message="The key is expired"):
        self.key = key
        self.message = message
        super().__init__(self.message)


class KeyDoesNotExistError(Exception):
    """
    An exception class to raise when a key does not exist.
    """

    def __init__(self, key, message="The key does not exist"):
        self.key = key
        self.message = message
        super().__init__(self.message)


class ExpirationType(Enum):
    """
    An Enum class to specify the type of expiration for the key.
    """

    TEMPORARY = "T"
    PERMANENT = "P"


class SaveType(Enum):
    """
    An Enum class to specify the type of data being saved to the redis connection.
    """

    NON_PICKLE = "non_pickle"
    PICKLE = "pickle"


SaveValueType = Any


class RedisClient:
    """
    A class used as a client for the redis databse.
    This creates a connection using a connnection pool and then allows us to execute functions.
    The first pool is for non pickle objects such as strings.
    The second is for nested dictionary objects.
    """

    def __init__(self):
        # https://stackoverflow.com/questions/32276493/how-to-store-and-retrieve-a-dictionary-with-redis
        # https://github.com/redis/redis-py/issues/809

        self._connection_pool_native: ConnectionPool = ConnectionPool(
            host=Environment.get_environment_variable(
                EnvironmentVariableKeys.REDIS_HOST
            ),
            port=Environment.get_environment_variable(
                EnvironmentVariableKeys.REDIS_PORT
            ),
            password=Environment.get_environment_variable(
                EnvironmentVariableKeys.REDIS_PASSWORD
            ),
            decode_responses=True,
        )
        self._connection_pool_pickle: ConnectionPool = ConnectionPool(
            host=Environment.get_environment_variable(
                EnvironmentVariableKeys.REDIS_HOST
            ),
            port=Environment.get_environment_variable(
                EnvironmentVariableKeys.REDIS_PORT
            ),
            password=Environment.get_environment_variable(
                EnvironmentVariableKeys.REDIS_PASSWORD
            ),
            decode_responses=False,
        )

        self.connection: Redis = Redis(connection_pool=self._connection_pool_native)
        self.pickle_connection: Redis = Redis(
            connection_pool=self._connection_pool_pickle
        )

    def __enter__(self) -> "RedisClient":
        """
        Allows us to setup a context manager with Redis Client.
        More specifically allowing us to use the redis connection that has been
        created with the connection pool.


        Returns
            A redis connection from the connection pool.
        """

        return self

    def __exit__(  # pylint: disable=redefined-builtin
        self, type, value, traceback
    ) -> None:
        pass

    def save(self, key: str, value: SaveValueType, expiration_time: int = -1) -> bool:
        """
        Saves a key to the redis connection.

        Args:
            key: A string representing the key to save.
            value: A string represting the value associated with the key.
            expiration_time: An optional paramter which can specify when the key will expire.

        Returns:
            A boolean which specifies if the key was successfully saved
        """

        save_value: SaveValueType = value
        save_type: SaveType = SaveType.NON_PICKLE

        if isinstance(value, (dict, list)):
            save_value = dumps(value)
            save_type = SaveType.PICKLE

            self.pickle_connection.set(key, save_value)

        else:
            self.connection.set(key, save_value)

        save_type_str: str = save_type.value
        # used internally to convert to the correct value type

        self.connection.set(self._get_type_key(key), save_type_str)

        expiration_key: str = self._get_expiration_key(key)

        if expiration_time == -1:
            self.connection.set(
                expiration_key,
                value=(ExpirationType.TEMPORARY.value),
                px=expiration_time,
            )
        else:
            self.connection.set(expiration_key, value=(ExpirationType.PERMANENT.value))

        return True

    def get(self, key: str) -> SaveValueType:
        """
        A method to get the value associated with the given key from redis.

        Args:
            key (str): The key of the value to retrieve.

        Raises:
            KeyError: The given key either did not exist or expired.

        Returns:
            any: The value associated with the given key.
        """

        type_key = self._get_type_key(key)

        if not self.connection.get(type_key):
            raise KeyDoesNotExistError("The key does not exist")

        expiration_key = self._get_expiration_key(key)
        expiration_value = self.connection.get(expiration_key)

        if expiration_value is None:
            self.remove_keys([key, type_key])
            raise KeyExpiredError("The key is expired")

        value: SaveValueType

        if self.connection.get(type_key) == "pickle":
            picked_value: SaveValueType = self.pickle_connection.get(key)
            value = loads(picked_value)
        else:
            value = self.connection.get(key)

        if value is None:
            raise KeyDoesNotExistError("The key does not exist")

        return value

    def remove_keys(self, keys: List[str]) -> None:
        """
        Delete Redis cache keys

        Args:
            keys (list): A list of cache keys to be deleted.

        Returns:
            None
        """

        for key in keys:
            self.connection.delete(key)

    def _get_type_key(self, key: str) -> str:
        return f"__type__{key}__"

    def _get_expiration_key(self, key: str) -> str:
        return f"__expiration__{key}__"

import pandas as pd
import redis
import logging


class SimResultsGetter:
    """
    Class gathering methods allowing the collection of results
    """

    def __init__(self):
        self.redis = None

    def connect_to_results_db(self, db=0, host="localhost", port=6379):
        """
        Instantiate connection with Redis DB

        :param db:
        :param host: host where the Redis container is running
        :param port: port where the Redis container is listening
        :return: nothing :)
        """
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        logging.info("Connected to {} Redis DB".format(host))

    @property
    def list_of_available_results(self):
        """
        :return: a pandas.DataFrame() describing the available results by nodes
        """
        keys = [k.decode("utf-8") for k in self.redis.keys() if "time" not in str(k)]
        return pd.DataFrame(
            [k.split("||") for k in keys], columns=["IN/OUT", "Node", "Attribute"]
        )

    def get_results_by_pattern(self, pattern, origin="2015-01-01"):
        """
        Allow to get results from a given name pattern

        :param pattern: the pattern used to query the Redis DB
        :param origin: start date for the simulation time index, default: '2015-01-01'
        :return: a dict mapping results name with pandas.Series() of values
        """
        matching_keys = [key.decode("utf-8") for key in self.redis.keys(pattern)]

        list_of_value = sorted([key for key in matching_keys if "time" not in key])
        list_of_index = sorted([key for key in matching_keys if "time" in key])

        res = {}

        for (key_v, key_t) in zip(list_of_value, list_of_index):
            value = list(map(float, self.redis.lrange(key_v, 0, -1)))
            index = list(map(float, self.redis.lrange(key_t, 0, -1)))

            index = pd.to_datetime(index, unit="s", origin=origin)

            res[key_v] = pd.Series(value, index=index)

        return res

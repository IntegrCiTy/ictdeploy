import pandas as pd
import redis
import logging


class SimResultsGetter:
    def __init__(self):
        self.redis = None

    def connect_to_results_db(self, db=0, host="172.17.01", port=6379):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        logging.info("Connected to {} Redis DB".format(host))

    @property
    def list_of_available_results(self):
        keys = [k.decode("utf-8") for k in self.redis.keys() if "time" not in str(k)]
        return pd.DataFrame([k.split('_') for k in keys], columns=["IN/OUT", "Node", "Attribute"])

    def get_results_by_pattern(self, pattern, origin='2015-01-01'):
        matching_keys = [key.decode("utf-8") for key in self.redis.keys(pattern)]

        list_of_value = sorted([key for key in matching_keys if 'time' not in key])
        list_of_index = sorted([key for key in matching_keys if 'time' in key])

        res = {}

        for (key_v, key_t) in zip(list_of_value, list_of_index):
            value = list(map(float, self.redis.lrange(key_v, 0, -1)))
            index = list(map(float, self.redis.lrange(key_t, 0, -1)))

            index = pd.to_datetime(index, unit='s', origin=origin)

            res[key_v] = pd.Series(value, index=index)

        return res

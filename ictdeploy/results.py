import pandas as pd
import redis
import logging


class SimResultsGetter:
    def __init__(self):
        self.redis = None

    def connect_to_db(self, db=0, host="localhost", port=6379):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        logging.info("Connected to {} Redis DB".format(host))

    @property
    def list_of_available_results(self):
        keys = [k.decode("utf-8") for k in self.redis.keys() if "time" not in str(k)]
        return pd.DataFrame([k.split('_') for k in keys], columns=["IN/OUT", "Node", "Attribute"])

    def get_results_by_pattern(self, pattern):
        return None

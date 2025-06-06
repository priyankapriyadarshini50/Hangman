"""
This module provides the facility to chache the frequently used data.
"""
import pickle
import redis
import logging
from django.core.cache import cache
django_logger = logging.getLogger('django')
class GameCache:
    '''caching the game data'''

    @staticmethod
    def set_to_cache(pk: int, value: dict):
        '''save to memcache'''
        try:
            pickled_data = pickle.dumps(value)
            cache.set(key=f'game_status_{pk}', value=pickled_data, timeout=120) # for testing
        except (pickle.PicklingError, redis.exceptions.ConnectionError) as p:
            django_logger.error("Pickling Error from REDIS Cache=%s", p, exc_info=1)

    @staticmethod
    def get_from_cache(pk: int):
        '''get the caching data from memcach'''
        try:
            cache_data = cache.get(key=f'game_status_{pk}')
            if cache_data is None:
                return None
            print('Getting from cache')
            return pickle.loads(cache_data)
        except (pickle.UnpicklingError, redis.exceptions.ConnectionError) as pe:
            django_logger.error("Unpicking ERROR from REDIS=%s", pe, exc_info=True)

# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from collective.address.behaviors import IAddress
from rohberg.bluechurch.content.bluechurchevent import IBluechurchevent


import logging
logger = logging.getLogger(__name__)


@indexer(IBluechurchevent)
def city_event(obj):
    """eventlocation/to_object/city
    """
    # logger.info('city_eventindexed: %r' % obj)
    # return u"Bremen"
    try:        
        loc = obj.eventlocation.to_object
        acc = IAddress(loc, None)
        c = acc.city
        return c
    except Exception as e:
        logger.error('index fail: %r' % e)
        
  
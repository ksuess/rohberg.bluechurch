# -*- coding: utf-8 -*-

from plone.indexer.decorator import indexer
from collective.address.behaviors import IAddress
from dexterity.membrane.behavior.user import INameFromFullName
# from dexterity.membrane.content.member import IMember
from rohberg.bluechurch.content.bluechurchevent import IBluechurchevent
from rohberg.bluechurch.content.bluechurchmembraneprofile import IBluechurchmembraneprofile

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
        logger.error('index fail: {}'.format(str(e)))
        
  

# @indexer(IBluechurchmembraneprofile)
# def Title(object, **kw):
#     name = INameFromFullName(object, None)
#     logger.info(u"indexer name: {} {}".format(name, name.title))
#     if name is not None:
#         return name.title
#     return object.Title()
#

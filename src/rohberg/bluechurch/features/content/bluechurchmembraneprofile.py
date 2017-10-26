from zope import schema
from plone import api
from plone.supermodel import model

# from Products.membrane.events import MembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent

from dexterity.membrane.content.member import IMember
from collective import dexteritytextindexer

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch.features import _

class IBluechurchmembraneprofile(IMember):
    """
    Artist or Event Manager
    """
    # TODO: make membrane fields searchable
    dexteritytextindexer.searchable('first_name')
    dexteritytextindexer.searchable('last_name')
    dexteritytextindexer.searchable('bio')
    
    model.load('bluechurchmembraneprofile.xml')
    
def setProfileRoles(profile, event):
    """Event handler"""
    # TODO: setProfileRoles
    logger.info("setProfileRoles")
    
    # granting role for adding content
    current = api.user.get_current()
    user = current
    logger.info(user)
    username = user.getName()
    roles = api.user.get_roles(username=username)
    
    logger.info(",".join(roles))
    api.user.grant_roles(username='jane', roles=['Bluechurch Member'])
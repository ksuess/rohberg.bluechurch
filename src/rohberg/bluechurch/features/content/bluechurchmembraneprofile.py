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
    
def setRoles(obj, event):
    """Event handler"""
    # TODO: setRoles for Profile
    logger.info("setRoles")
    
    # # granting role for adding content
    # current = api.user.get_current()
    # if current:
    #     user = current
    #     logger.info(user)
    #     username = user.getName()
    #     roles = api.user.get_roles(username=username)
    #
    #     logger.info(",".join(roles))
    #     api.user.grant_roles(username=username, roles=['Bluechurch Member'])
        
        
from Products.membrane.interfaces import IMembraneUserRoles
from dexterity.membrane.behavior.user import DxUserObject
from dexterity.membrane.behavior.membraneuser import IMembraneUser
from zope.component import adapter
from zope.interface import implementer

DEFAULT_ROLES = ['Bluechurch Member', 'Member']


@implementer(IMembraneUserRoles)
@adapter(IMembraneUser)
class MyDefaultRoles(DxUserObject):

     def getRolesForPrincipal(self, principal, request=None):
         return DEFAULT_ROLES
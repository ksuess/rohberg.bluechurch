from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implementer
from plone import api
from plone.autoform import directives
from plone.supermodel import model
from plone.dexterity.content import Item

# from Products.membrane.events import MembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent

from dexterity.membrane.content.member import IMember
from collective import dexteritytextindexer

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch.features import _

profile_types = SimpleVocabulary(
    [SimpleTerm(value=u'artist', title=_(u'Artist')),
     SimpleTerm(value=u'eventmanager', title=_(u'Event Manager'))]
    )

class IBluechurchmembraneprofile(IMember):
    """
    Artist or Event Manager
    """
    # TODO: make membrane fields searchable
    dexteritytextindexer.searchable('first_name')
    dexteritytextindexer.searchable('last_name')
    dexteritytextindexer.searchable('bio')
    
    # directives.widget('select_field', SelectWidget)
    profile_type = schema.Choice(
                title=_(u"Profil-Typ"),
                vocabulary=profile_types,
                required=True,
                default="artist",
            )
    
    model.load('bluechurchmembraneprofile.xml')



@implementer(IBluechurchmembraneprofile)
class Bluechurchmembraneprofile(Item):
    """
    """
    
    
        
def setInitialProfileRoles(obj, event):
    """Event handler"""
    # TODO: setInitialProfileRoles for Profile
    logger.info("setInitialProfileRoles")
    
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
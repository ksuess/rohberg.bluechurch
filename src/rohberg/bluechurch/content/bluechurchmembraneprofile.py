from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import adapter
from zope.interface import implementer
from plone import api
from plone.autoform import directives
from plone.supermodel import model
from plone.dexterity.content import Item

        
from Products.membrane.interfaces import IMembraneUserRoles
from dexterity.membrane.behavior.user import DxUserObject
from dexterity.membrane.behavior.membraneuser import IMembraneUser

# from Products.membrane.events import MembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent

from dexterity.membrane.content.member import IMember
from collective import dexteritytextindexer

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _

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
    zip_code = schema.TextLine(
        title=_(u'label_zip_code', default=u'Zip Code'),
        description=_(u'help_zip_code', default=u''),
        required=False
    )
    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city', default=u''),
        required=False
    )
    country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country',
                      default=u'Select the country from the list.'),
        required=False,
        vocabulary='collective.address.CountryVocabulary'
    )
    
    model.load('bluechurchmembraneprofile.xml')



@implementer(IBluechurchmembraneprofile)
class Bluechurchmembraneprofile(Item):
    """
    """
    
    
        
def setInitialProfileRoles(obj, event):
    """Event handler"""
    # TODO: setInitialProfileRoles for Profile
    # import pdb; pdb.set_trace()
    logger.info("setInitialProfileRoles")
    username = obj.UID
    logger.info(username)
    
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
    
    ploneuser = api.user.get(username)
    logger.info(ploneuser)
    # api.user.grant_roles(username=username, roles=['Bluechurch Member'])
        


DEFAULT_ROLES = ['Bluechurch Member', 'Member']
# DEFAULT_ROLES = ['Member',]

@implementer(IMembraneUserRoles)
# @adapter(IMembraneUser)
@adapter(IBluechurchmembraneprofile)
class MyDefaultRoles(DxUserObject):

     def getRolesForPrincipal(self, principal, request=None):
         return DEFAULT_ROLES

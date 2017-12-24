from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import adapter
from zope.interface import implementer
from plone import api
from plone.autoform.directives import widget
from plone.supermodel import model
from plone.dexterity.content import Item
from z3c.form.interfaces import IAddForm, IEditForm
from plone.autoform import directives
from z3c.form.browser.checkbox import CheckBoxFieldWidget
        
from Products.membrane.interfaces import IMembraneUserRoles
from dexterity.membrane.behavior.user import DxUserObject
from dexterity.membrane.behavior.membraneuser import IMembraneUser

# from Products.membrane.events import MembraneTypeRegisteredEvent
from Products.membrane.interfaces.events import IMembraneTypeRegisteredEvent

from dexterity.membrane.content.member import IMember
from collective import dexteritytextindexer
from dexterity.membrane.behavior.password import IProvidePasswords
from dexterity.membrane.behavior.user import INameFromFullName

from rohberg.bluechurch.fields import URI_bluechurch

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _

profile_types = SimpleVocabulary(
    [SimpleTerm(value=u'artist', title=_(u'Artist')),
        SimpleTerm(value=u'band', title=_(u'Band')),
        SimpleTerm(value=u'theologian', title=_(u'Theologian')),
        SimpleTerm(value=u'interested', title=_(u'Interested Person')),
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
    
    website = URI_bluechurch(
        title=_(u"Website"),
        description = _(u"e.g. www.abcjazzz.com"),
        required = False,
    )
    
    widget(profile_type='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    profile_type = schema.Set(
                title=_(u"Profile Type"),
                value_type=schema.Choice(
                    vocabulary=profile_types),
                required=True,
            )
    
    directives.widget(bluechurchtags='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    bluechurchtags = schema.Set(
        title=_(u'Bluechurch Tags'),
        value_type=schema.Choice(
            vocabulary='rohberg.bluechurch.BluchurchTags'),
        required=False,
        )
        
    zip_code = schema.TextLine(
        title=_(u'label_zip_code', default=u'Zip Code'),
        description=_(u'help_zip_code', default=u''),
        required=True
    )
    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city', default=u''),
        required=True
    )
    country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country',
                      default=u'Select the country from the list.'),
        required=True,
        vocabulary='collective.address.CountryVocabulary'
    )
    
    bluechurchcaptcha = schema.Int(
        title=_(u"bluechurchcaptcha"),
        description=_(u"Prevent spam by typing in the result of 13 + 4."),
        min=17,
        max=17
    )
    directives.omitted('bluechurchcaptcha')
    directives.no_omit(IAddForm, 'bluechurchcaptcha')
    
    model.fieldset(
        'categorization',
        label=_(u'Relations')
    )
    
    # directives.omitted('relatedItems')
    # directives.no_omit(IEditForm, 'relatedItems')
    
    model.load('bluechurchmembraneprofile.xml')

# modifications Artist Profile
IBluechurchmembraneprofile['last_name'].title = _(u"Last Name or Band Name")
IBluechurchmembraneprofile['first_name'].title = _(u"First Name")
IBluechurchmembraneprofile['first_name'].required = False

IBluechurchmembraneprofile['email'].title = _(u"E-mail Address")
IBluechurchmembraneprofile['homepage'].title = _(u"Website")
IBluechurchmembraneprofile['homepage'].description = _(u"e.g. http://www.abcjazzz.com")
IBluechurchmembraneprofile['bio'].title = _(u"Biography")

IProvidePasswords['password'].required = True
IProvidePasswords['password'].title = _(u"Password")
IProvidePasswords['confirm_password'].required = True
IProvidePasswords['confirm_password'].title = _(u"Confirm Password")

from collective.address.behaviors import ISocial
ISocial['facebook_url'].description = _(u"e.g. www.facebook.com/myprofile")
ISocial['twitter_url'].description = _(u"e.g. www.twitter.com/myprofile")
ISocial['google_plus_url'].description = _(u"e.g. plus.google.com/myprofile")
ISocial['instagram_url'].description = _(u"e.g. www.instagram.com/myprofile")

@implementer(IBluechurchmembraneprofile)
class Bluechurchmembraneprofile(Item):
    """
    """
    def Title(self):
        return INameFromFullName(self).title

    @property
    def title(self):
        return INameFromFullName(self).title
    
    
        
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

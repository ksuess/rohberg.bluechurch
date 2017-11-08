from zope import schema
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

from Products.CMFCore.interfaces import IDublinCore
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model


from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel.interfaces import IDefaultFactory
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from Products.CMFCore.utils  import getToolByName
from rohberg.bluechurch.content import IBluechurchmembraneprofile

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _

# TODO: clean up get basePath
def get_profiles_base_path(context=None):
    path = '/'.join(getSite().getPhysicalPath())
    path += '/web/profiles'
    return path
    
def get_locations_base_path(context=None):
    path = '/'.join(getSite().getPhysicalPath())
    path += '/web/locations'
    return path
    
@provider(IDefaultFactory)
# @provider(IContextAwareDefaultFactory)
def profile_current_user():
    logger.info("profile_current_user")
    logger.debug("profile_current_user")
    # logger.info(context)
    # if context.kontaktperson:
    #     return
    current = api.user.get_current()
    if api.user.is_anonymous():
        logger.info("profile_current_user")
        logger.info(current)
        logger.warn("is_anonymous. why?")
        return None
    current_roles = api.user.get_roles(user=current)
    if not "Manager" in current_roles and not "Site Administrator" in current_roles:
        try:
            profile = api.content.get(UID=current.id)
            logger.info(profile)
            logger.info(profile.portal_type)
            logger.info(IBluechurchmembraneprofile.providedBy(profile))
        except Exception, e:
            logger.error(str(e) + u"No profile found with UID {}".format(current.id))
    else:
        profile = None
    return profile
        

@provider(IFormFieldProvider)
class IOwnercontact(model.Schema):
    """Add kontaktperson to content
    """
    
    # Kontaktperson
    # TODO: Default Kontaktperson
    kontaktperson = RelationChoice(
        title=_(u"Kontaktperson"),
        required=True,
        # source=CatalogSource(portal_type='dexterity.membrane.bluechurchmembraneprofile'),
        # source=ObjPathSourceBinder(
        #     portal_type="dexterity.membrane.bluechurchmembraneprofile",
        #     navigation_tree_query=dict(
        #         portal_type=["dexterity.membrane.bluechurchmembraneprofile",],
        #         path={ "query": '/web/profiles' })
        # ),
        vocabulary='plone.app.vocabularies.Catalog',
        defaultFactory=profile_current_user,
        )
    widget(
        'kontaktperson',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['dexterity.membrane.bluechurchmembraneprofile',],
            'mode': 'search',
            'basePath': get_profiles_base_path,
        }
        )
    # fieldset(
    #     'categorization',
    #     label=_(u'Categorization'),
    #     fields=['kontaktperson']
    # )
    
    
    # kontaktperson = RelationChoice(
    #     title=_(u"Kontaktperson"),
    #     required=True,
    #     source=CatalogSource(portal_type='dexterity.membrane.bluechurchmembraneprofile'),
    #     # vocabulary='plone.app.vocabularies.Catalog',
    #     defaultFactory=profile_current_user
    #     )
    # widget(
    #     'kontaktperson',
    #     RelatedItemsFieldWidget,
    #     pattern_options={
    #         'selectableTypes': ['dexterity.membrane.bluechurchmembraneprofile',],
    #         # 'mode': 'search',
    #         'basePath': get_site,
    #     }
    #     )



def setLocalRolesOnBluechurchObjects(obj, event):
    """ Set Role Owner to new kontaktperson (event handler on creation and modification)"""

    logger.info("setLocalRolesOnBluechurchObjects")
    
    kp = obj.kontaktperson
    logger.info(kp)
    # import pdb; pdb.set_trace()
    if not kp:
        return
    username = kp.to_object.UID()
    logger.info(username)
    ploneuser = api.user.get(username)
    logger.info(ploneuser)

    # obj.changeOwnership(ploneuser)
    for otherusername, roles in obj.get_local_roles():
        obj.manage_delLocalRoles([otherusername])
    api.user.grant_roles(username=username, obj=obj, roles=["Owner",])
    
    # current = api.user.get_current()
    # current_roles = api.user.get_roles(user=current)
    # if not "Manager" in current_roles and not "Site Administrator" in current_roles:
    #     api.user.revoke_roles(user=current, obj=obj, roles=["Owner",])
    
    # local roles:
    # logger.info(api.user.get_roles(user=current, obj=obj))
    

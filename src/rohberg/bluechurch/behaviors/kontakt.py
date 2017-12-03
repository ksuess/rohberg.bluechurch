from zope import schema
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import provider
from zope.interface import Interface
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

from rohberg.bluechurch.content.bluechurchmembraneprofile import IBluechurchmembraneprofile
from rohberg.bluechurch.utils import get_profiles_base_path

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _

    
@provider(IDefaultFactory)
# @provider(IContextAwareDefaultFactory)
def profile_current_user():
    current = api.user.get_current()
    logger.info("current user {}".format(current))
    
    if api.user.is_anonymous():
        logger.warn("profile_current_user: is_anonymous True. Should not happen. User is logged in")
        return None
        

    current_roles = api.user.get_roles(user=current)
    if not "Manager" in current_roles and not "Site Administrator" in current_roles:
        try:
            profile = api.content.get(UID=current.id)
            logger.info("current users profile: " + str(profile))
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
    read_permission(kontaktperson='zope2View')
    write_permission(kontaktperson='rohberg.bluechurch.addbluechurchcontent')
    kontaktperson = RelationChoice(
        title=_(u"Kontaktperson"),
        description=_(u"Kontaktperson"),
        required=True,
        # source=CatalogSource(portal_type='dexterity.membrane.bluechurchmembraneprofile'),
        # source=ObjPathSourceBinder(
        #     portal_type="dexterity.membrane.bluechurchmembraneprofile",
        #     navigation_tree_query=dict(
        #         portal_type=["dexterity.membrane.bluechurchmembraneprofile",],
        #         path={ "query": '/profiles' })
        # ),
        vocabulary='plone.app.vocabularies.Catalog',
        defaultFactory=profile_current_user,
        )
    # order_after(notes='*')
    widget(
        'kontaktperson',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['dexterity.membrane.bluechurchmembraneprofile',],
            'basePath': get_profiles_base_path,
        }
        )
        
    model.fieldset(
        'categorization',
        label=_(u'Relations'),
        fields=['kontaktperson']
    )
    


class IOwnercontactMarker(Interface):
    """Marker interface that will be provided by instances using the
    IOwnercontact behavior. The eventsubscribers foo and bar are registered for
    this marker.
    """

def setLocalRolesOnBluechurchObjects(obj, event):
    """ Set Role Owner to new or edited kontaktperson 
    (event handler on creation and modification)
    other local roles on this objects are removed!
    """

    logger.info("*** setLocalRolesOnBluechurchObjects")
    
    kp = obj.kontaktperson
    if not kp:
        return
    profile = kp.to_object
    username = profile.UID()
    ploneuser = api.user.get(username)
    for otherusername, roles in obj.get_local_roles():
        obj.manage_delLocalRoles([otherusername])
    api.user.grant_roles(username=username, obj=obj, roles=["Owner",])
    
    # logger.info("local role 'Owner' auf Objekt {} an {} mit UID {} vergeben".format(str(obj), profile, username))
    
    # current = api.user.get_current()
    # current_roles = api.user.get_roles(user=current)
    # if not "Manager" in current_roles and not "Site Administrator" in current_roles:
    #     api.user.revoke_roles(user=current, obj=obj, roles=["Owner",])
    
    # local roles:
    # logger.info(api.user.get_roles(user=current, obj=obj))
    

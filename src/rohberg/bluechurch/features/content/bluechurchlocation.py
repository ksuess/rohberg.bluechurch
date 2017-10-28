# coding: utf-8
from zope import schema
from zope.interface import implementer
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.autoform import directives
from Products.CMFCore.utils  import getToolByName

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch.features import _

class IBluechurchlocation(model.Schema):
    """ Marker interface for Bluechurchlocation
    """

    # Kontaktperson
    # TODO: Default fuer kontaktperson: current user
    widget(
        'kontaktperson',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['dexterity.membrane.bluechurchmembraneprofile']
        }
        )
    kontaktperson = schema.Choice(
        title=_(u"Kontaktperson"),
        required=True,
        vocabulary='plone.app.vocabularies.Catalog',
        )
    
    model.load('bluechurchlocation.xml')


@implementer(IBluechurchlocation)
class Bluechurchlocation(Item):
    """
    """

def setRoles(obj, event):
    """ Set Role Owner to new kontaktperson"""
    
    uidkontaktperson = obj.kontaktperson 
    username = uidkontaktperson    
    ploneuser = api.user.get(username)

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
    
    
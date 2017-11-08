# coding: utf-8
from zope import schema
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import provider
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.supermodel.interfaces import IDefaultFactory
from zope.schema.interfaces import IContextAwareDefaultFactory
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.autoform import directives
from Products.CMFCore.utils  import getToolByName
from rohberg.bluechurch.content import IBluechurchmembraneprofile

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _

def get_site(context=None):
    return '/'.join(getSite().getPhysicalPath())


class IBluechurchlocation(model.Schema):
    """ Marker interface for Bluechurchlocation
    """    
    model.load('bluechurchlocation.xml')


@implementer(IBluechurchlocation)
class Bluechurchlocation(Item):
    """
    """

    
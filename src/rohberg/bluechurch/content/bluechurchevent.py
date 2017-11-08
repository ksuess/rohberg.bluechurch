# -*- coding: utf-8 -*-
from zope import schema
from zope.component.hooks import getSite
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _

# TODO: clean up get_locations_base_path. Nicht fest verdrahtet
def get_locations_base_path(context=None):
    path = '/'.join(getSite().getPhysicalPath())
    path += '/web/locations'
    return path

class IBluechurchevent(model.Schema):
    """ Marker interface for Bluechurchevent
    """
        
    #TODO: Location
    location = RelationChoice(
        title=_(u"Location"),
        required=True,
        vocabulary='plone.app.vocabularies.Catalog',
        )
    widget(
        'location',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['bluechurchlocation',],
            'mode': 'search',
            'basePath': get_locations_base_path,
        }
        )
        
    model.load('bluechurchevent.xml')

@implementer(IBluechurchevent)
class Bluechurchevent(Item):
    """
    """

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

# TODO: clean up get basePath
def get_profiles_base_path(context=None):
    path = '/'.join(getSite().getPhysicalPath())
    path += '/web/profiles'
    return path
    
def get_locations_base_path(context=None):
    path = '/'.join(getSite().getPhysicalPath())
    path += '/web/locations'
    return path

class IBluechurchevent(model.Schema):
    """ Marker interface for Bluechurchevent
    """
    # kontaktperson = RelationChoice(
    #     title=_(u"Kontaktperson"),
    #     required=True,
    #     vocabulary='plone.app.vocabularies.Catalog',
    #     # defaultFactory=profile_current_user,
    #     )
    # widget(
    #     'kontaktperson',
    #     RelatedItemsFieldWidget,
    #     pattern_options={
    #         'selectableTypes': ['dexterity.membrane.bluechurchmembraneprofile',],
    #         'mode': 'search',
    #         'basePath': "/web/profiles",
    #     }
    #     )
        
    #TODO: Location
    location = RelationChoice(
        title=_(u"Location"),
        required=True,
        vocabulary='plone.app.vocabularies.Catalog',
        # defaultFactory=profile_current_user,
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

# -*- coding: utf-8 -*-
from zope import schema
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch.features import _


class IBluechurchevent(model.Schema):
    """ Marker interface for Bluechurchevent
    """
    
    #TODO: Location
    location = RelationChoice(
        title=_(u"Location"),
        required=True,
        # source=CatalogSource(portal_type='dexterity.membrane.bluechurchmembraneprofile'),
        # source=ObjPathSourceBinder(
        #     portal_type="dexterity.membrane.bluechurchmembraneprofile",
        #     navigation_tree_query=dict(
        #         portal_type=["dexterity.membrane.bluechurchmembraneprofile",],
        #         path={ "query": '/web/profiles' })
        # ),
        vocabulary='plone.app.vocabularies.Catalog',
        # defaultFactory=profile_current_user,
        )
    widget(
        'location',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['bluechurchlocation',],
            'mode': 'search',
            'basePath': "/web/locations",
        }
        )
        
    model.load('bluechurchevent.xml')

@implementer(IBluechurchevent)
class Bluechurchevent(Item):
    """
    """

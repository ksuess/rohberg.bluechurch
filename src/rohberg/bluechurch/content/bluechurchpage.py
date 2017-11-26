# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implementer
from zope.interface import implements
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer

from rohberg.bluechurch.content.interfaces import IBluechurchMemberContent
from rohberg.bluechurch.utils import get_profiles_base_path, get_locations_base_path

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _


class IBluechurchpage(model.Schema):
    """ Marker interface for Bluechurchpage
    """
    
    beteiligte = RelationList(
        title=_(u"Artists"),
        description=_(u"Beteiligte Artists, Veranstalter"),
        required=False,
        value_type=RelationChoice(
                vocabulary='plone.app.vocabularies.Catalog',
                )
        )
    widget(
        'beteiligte',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['dexterity.membrane.bluechurchmembraneprofile',],
            'mode': 'search',
            'basePath': get_profiles_base_path,
        }
        )
        
    model.load('bluechurchpage.xml')


@implementer(IBluechurchpage)
class Bluechurchpage(Item):
    """
    """
    implements(IBluechurchMemberContent)

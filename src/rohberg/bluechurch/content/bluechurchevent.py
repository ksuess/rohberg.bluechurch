# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implements
from zope.component.hooks import getSite
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from plone.event.interfaces import IEventAccessor
from plone.app.event.dx.behaviors import EventAccessor

# from plone.formwidget.contenttree import ContentTreeFieldWidget
# from plone.formwidget.contenttree import MultiContentTreeFieldWidget
# from plone.formwidget.contenttree import PathSourceBinder
# from plone.formwidget.contenttree import UUIDSourceBinder

from rohberg.bluechurch.content.interfaces import IBluechurchMemberContent
from rohberg.bluechurch.utils import get_profiles_base_path, get_locations_base_path

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _


class IBluechurchevent(model.Schema):
    """ Marker interface for Bluechurchevent
    """
        
    eventlocation = RelationChoice(
        title=_(u"Location"),
        required=True,
        vocabulary='plone.app.vocabularies.Catalog',
        )
    widget(
        'eventlocation',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['bluechurchlocation',],
            'basePath': get_locations_base_path,
            }
        )
# pattern_options:
# 'mode': 'search',
# 'basePath': get_locations_base_path,


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
            'basePath': get_profiles_base_path,
            }
        )
        
    homepage = schema.URI(
        title=_(u"Website"),
        description = _(u"e.g. http://www.abcjazzz.com"),
        required = False,
    )
      
    bluechurchtags = schema.Set(
        title=_(u'Bluechurch Tags'),
        value_type=schema.Choice(
            vocabulary='rohberg.bluechurch.BluchurchTags'),
        required=False,
        )
    
    eventformen = schema.Set(
        title=_(u'Event Type'),
        value_type=schema.Choice(
            vocabulary='rohberg.bluechurch.Eventformen'),
        required=False,
        )
    
    model.fieldset(
        'categorization',
        fields=['beteiligte', 'eventlocation']
    )
# pattern_options:
# 'mode': 'search',
# 'basePath': get_profiles_base_path,

    model.load('bluechurchevent.xml')



@implementer(IBluechurchevent)
class Bluechurchevent(Item):
    """
    """
    implements(IBluechurchMemberContent)



@adapter(IBluechurchevent)
@implementer(IEventAccessor)
class BluechurchEventAccessor(EventAccessor):


    def __init__(self, context):
        super(BluechurchEventAccessor, self).__init__(context)
        
    def location(self):
        logger.info("BluechurchEventAccessor location")
        
        context = self.context
        lct = self.context.eventlocation
        return lct 
               
    def city(self):
        logger.info("BluechurchEventAccessor city")
        
        context = self.context
        lct = self.context.eventlocation
        ct = lct.to_object.city
        logger.info(ct)
        return ct
# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import implements
from zope.component.hooks import getSite
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.autoform.directives import widget
from plone.autoform import directives
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

from plone.app.event.dx.behaviors import IEventBasic

from rohberg.bluechurch.content.interfaces import IBluechurchMemberContent
from rohberg.bluechurch.utils import get_profiles_base_path, get_locations_base_path

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _


class IBluechurchevent(model.Schema):
    """ Marker interface for Bluechurchevent
    """
        
    # eventlocation = RelationChoice(
    #     title=_(u"Location"),
    #     required=True,
    #     vocabulary='plone.app.vocabularies.Catalog',
    #     )
    # widget(
    #     'eventlocation',
    #     RelatedItemsFieldWidget,
    #     pattern_options={
    #         'selectableTypes': ['bluechurchlocation',],
    #         'basePath': get_locations_base_path,
    #         }
    #     )
    
    directives.order_after(city='IEventLocation.location')
    city = schema.TextLine(
        title=_(u'label_city', default=u'City'),
        description=_(u'help_city', default=u''),
        required=True
    )
    
    directives.order_after(country='city')
    country = schema.Choice(
        title=_(u'label_country', default=u'Country'),
        description=_(u'help_country',
                      default=u'Select the country from the list.'),
        required=True,
        vocabulary='collective.address.CountryVocabulary'
    )
        
    # beteiligte = RelationList(
    #     title=_(u"Artists"),
    #     description=_(u"Beteiligte Artists, Veranstalter"),
    #     required=False,
    #     value_type=RelationChoice(
    #         vocabulary='plone.app.vocabularies.Catalog',
    #         )
    #     )
    # widget(
    #     'beteiligte',
    #     RelatedItemsFieldWidget,
    #     pattern_options={
    #         'selectableTypes': ['dexterity.membrane.bluechurchmembraneprofile',],
    #         'basePath': get_profiles_base_path,
    #         }
    #     )
        
    # homepage = schema.URI(
    #     title=_(u"Website"),
    #     description = _(u"e.g. http://www.abcjazzz.com"),
    #     required = False,
    # )
      
    # widget(bluechurchtags='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    # bluechurchtags = schema.Set(
    #     title=_(u'Bluechurch Tags'),
    #     value_type=schema.Choice(
    #         vocabulary='rohberg.bluechurch.BluchurchTags'),
    #     required=False,
    #     )
    
      
    widget(eventformen='z3c.form.browser.checkbox.CheckBoxFieldWidget')
    eventformen = schema.Set(
        title=_(u'Event Type'),
        value_type=schema.Choice(
            vocabulary='rohberg.bluechurch.Eventformen'),
        required=False,
        )
    
    # model.fieldset(
    #     'categorization',
    #     label=_(u'Relations'),
    #     # fields=['beteiligte', 'eventlocation']
    # )
    
    model.load('bluechurchevent.xml')



IEventBasic['open_end'].default = True

@implementer(IBluechurchevent)
class Bluechurchevent(Item):
    """
    """
    implements(IBluechurchMemberContent)


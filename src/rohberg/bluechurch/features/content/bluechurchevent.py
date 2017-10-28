# -*- coding: utf-8 -*-
from zope import schema
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.directives import widget
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IBluechurchevent(model.Schema):
    """ Marker interface for Bluechurchevent
    """

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
        
    model.load('bluechurchevent.xml')

@implementer(IBluechurchevent)
class Bluechurchevent(Item):
    """
    """

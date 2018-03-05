# -*- coding: utf-8 -*-
from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.directives import order_after
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from rohberg.bluechurch.utils import get_site_path
from rohberg.bluechurch.vocabularies import default_map_layer
from rohberg.bluechurch.vocabularies import default_map_layers

from rohberg.bluechurch import _

class IBluechurchControlPanel(Interface):

    # TODO widget for bluechurchtags
    # form.widget(bluechurchtags=AjaxSelectWidget)
    bluechurchtags = schema.List(
        title=u'Schlagworte',
        description=u'Schlagworte, Tags, ',
        value_type=schema.TextLine(),
        default=["Spiritual Jazz/Sacred Jazz", "Dixie", "Swing", "Bebop", "Latin", "Cool Jazz", "Kinder", "Ethno"]
    )
    
    eventformen = schema.List(
        title=u'Eventformen',
        description=u'Jazzgottesdienst, etc',
        value_type=schema.TextLine(),
        default=["Jazzgottesdienst", "Liturgischer Jazz", "Konzert", "Workshop"],
    )
    
    profiles_base = schema.TextLine(
        title=_(u"Profiles Folder"),
        default=u"",
        required=False,
    )
    locations_base = schema.TextLine(
        title=_(u"Locations Folder"),
        default=u"",
        required=False,
    )
    
    
    default_map_layer = schema.Choice(
        title=_(
            u'default_map_layer',
            u'Default map layer'
        ),
        description=_(
            u'help_default_map_layer',
            default=u'Set the default map layer'
        ),
        required=False,
        default=default_map_layer,
        vocabulary='rohberg.bluechurch.map_layers'
    )

    map_layers = schema.List(
        title=_(u'label_map_layers', u'Map Layers'),
        description=_(
            u'help_map_layers',
            default=u'Set the available map layers'),
        required=False,
        default=default_map_layers,
        missing_value=[],
        value_type=schema.Choice(vocabulary='rohberg.bluechurch.map_layers'))
        
        
    GTMCode = schema.TextLine(
        title=u'GTMCode',
        description=u'Google Tag Manager Code',
        required=False,
    )
    

    google_api_key = schema.TextLine(
        title=_(u'label_google_api_key', default=u'Google maps API Key'),
        description=_(u'help_google_api_key', 
            default=u'If you want to use the Google Maps search API for higher accuracy, you have to provide a Google Maps API key here.'),  
        required=False,
        default=None
    )

class BluechurchControlPanelForm(RegistryEditForm):
    """schema_prefix must be the same than that in registry.xml in profiles"""
    schema = IBluechurchControlPanel
    schema_prefix = "rohberg.bluechurch"
    label = u'Bluechurch Settings'


BluechurchControlPanelView = layout.wrap_form(
    BluechurchControlPanelForm, ControlPanelFormWrapper)

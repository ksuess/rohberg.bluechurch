# -*- coding: utf-8 -*-
from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IBluechurchControlPanel(Interface):

    # TODO widget for bluechurchtags
    # form.widget(bluechurchtags=AjaxSelectWidget)
    bluechurchtags = schema.List(
        title=u'Schlagworte',
        description=u'Schlagworte, Tags, ',
        value_type=schema.TextLine(),
        default=["Familie"],
    )
    GTMCode = schema.TextLine(
        title=u'GTMCode',
        description=u'Google Tag Manager Code',
        required=False,
    )
    # farbe = schema.TextLine(
    #     title=u'Farbe',
    #     required=False,
    # )
    # motive = schema.List(
    #     title=u'Motive',
    #     description=u"Lorem ipsum tralllalalal",
    # )


class BluechurchControlPanelForm(RegistryEditForm):
    """schema_prefix must be the same than that in registry.xml in porfiles"""
    schema = IBluechurchControlPanel
    schema_prefix = "bluechurch"
    label = u'Bluechurch Settings'


BluechurchControlPanelView = layout.wrap_form(
    BluechurchControlPanelForm, ControlPanelFormWrapper)

# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from rohberg.bluechurch.features import _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
# from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IRohbergBluechurchFeaturesLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""



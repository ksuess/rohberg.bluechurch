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



class IBluechurchProfile(model.Schema):

    """A conference session. Sessions are managed inside Programs."""

    title = schema.TextLine(
        title=_(u'Title'),
    )

    description = schema.Text(
        title=_(u'Summary'),
    )

    details = RichText(
        title=_(u'Details'),
        required=False
    )


class IBluechurchEvent(model.Schema):

    """A conference session. Sessions are managed inside Programs."""

    title = schema.TextLine(
        title=_(u'Title'),
    )

    description = schema.Text(
        title=_(u'Summary'),
    )

    details = RichText(
        title=_(u'Details'),
        required=False
    )


class IBluechurchLocation(model.Schema):

    """A conference session. Sessions are managed inside Programs."""

    title = schema.TextLine(
        title=_(u'Title'),
    )

    description = schema.Text(
        title=_(u'Summary'),
    )

    details = RichText(
        title=_(u'Details'),
        required=False
    )


class IBluechurchdoc(model.Schema):

    """A conference session. Sessions are managed inside Programs."""

    title = schema.TextLine(
        title=_(u'Title'),
    )

    description = schema.Text(
        title=_(u'Summary'),
    )

    details = RichText(
        title=_(u'Details'),
        required=False
    )


class IBluechurchInserat(model.Schema):

    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )

    description = schema.Text(
        required=False,
    )

    details = RichText(
        title=_(u'Details'),
        required=False
    )
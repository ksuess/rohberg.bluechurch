# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IBluechurchevent(model.Schema):
    """ Marker interface for Bluechurchevent
    """


@implementer(IBluechurchevent)
class Bluechurchevent(Item):
    """
    """

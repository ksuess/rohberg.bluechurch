# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IBluechurchpage(model.Schema):
    """ Marker interface for Bluechurchpage
    """


@implementer(IBluechurchpage)
class Bluechurchpage(Item):
    """
    """

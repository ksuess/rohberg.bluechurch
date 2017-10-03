# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IBluechurchlocation(model.Schema):
    """ Marker interface for Bluechurchlocation
    """


@implementer(IBluechurchlocation)
class Bluechurchlocation(Item):
    """
    """

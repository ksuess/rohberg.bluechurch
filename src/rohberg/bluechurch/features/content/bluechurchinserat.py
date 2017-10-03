# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IBluechurchinserat(model.Schema):
    """ Marker interface for Bluechurchinserat
    """


@implementer(IBluechurchinserat)
class Bluechurchinserat(Item):
    """
    """

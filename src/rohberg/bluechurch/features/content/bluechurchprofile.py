# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IBluechurchprofile(model.Schema):
    """ Marker interface for Bluechurchprofile
    """


@implementer(IBluechurchprofile)
class Bluechurchprofile(Item):
    """
    """

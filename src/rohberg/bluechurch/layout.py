""" Override the default Plone layout utility.
"""
import random
from zope.component import queryUtility
from zope.component import getMultiAdapter

from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.app.layout.globals import layout as base
from plone.app.layout.navigation.interfaces import INavigationRoot


class LayoutPolicy(base.LayoutPolicy):
    """
    Enhanced layout policy helper.

    Extend the Plone standard class to have some more <body> CSS classes
    based on the current context.
    """

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag.
        """
        num = random.randint(1, 17)
        bg_class = "bg_" + str(num)
        bc = super(LayoutPolicy, self).bodyClass(template, view)
        return bc + " " + bg_class
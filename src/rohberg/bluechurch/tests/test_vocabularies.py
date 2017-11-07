# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from plone import api
from rohberg.bluechurch.testing import ROHBERG_BLUECHURCH_FEATURES_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that rohberg.bluechurch is properly installed."""

    layer = ROHBERG_BLUECHURCH_FEATURES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        # self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_values(self):
        bctags = queryUtility(IVocabularyFactory, name='rohberg.bluechurch.BluchurchTags')
        self.assertTrue(isinstance(bctags(), SimpleVocabulary))


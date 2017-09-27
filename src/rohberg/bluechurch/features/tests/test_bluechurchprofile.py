# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from rohberg.bluechurch.features.content.bluechurchprofile import IBluechurchprofile
from rohberg.bluechurch.features.testing import ROHBERG_BLUECHURCH_FEATURES_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class BluechurchprofileIntegrationTest(unittest.TestCase):

    layer = ROHBERG_BLUECHURCH_FEATURES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='bluechurchprofile')
        schema = fti.lookupSchema()
        schema_name = "plone_0_bluechurchprofile"
        self.assertEqual(schema_name, schema.getName())

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='bluechurchprofile')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='bluechurchprofile')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IBluechurchprofile.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='bluechurchprofile',
            id='bluechurchprofile',
        )
        self.assertTrue(IBluechurchprofile.providedBy(obj))

# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from rohberg.bluechurch.features.interfaces import IInserat
from rohberg.bluechurch.features.testing import ROHBERG_BLUECHURCH_FEATURES_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class InseratIntegrationTest(unittest.TestCase):

    layer = ROHBERG_BLUECHURCH_FEATURES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Inserat')
        schema = fti.lookupSchema()
        self.assertEqual(IInserat, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Inserat')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Inserat')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IInserat.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Inserat',
            id='Inserat',
        )
        self.assertTrue(IInserat.providedBy(obj))

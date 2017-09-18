# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import rohberg.bluechurch.features


class RohbergBluechurchFeaturesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=rohberg.bluechurch.features)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rohberg.bluechurch.features:default')


ROHBERG_BLUECHURCH_FEATURES_FIXTURE = RohbergBluechurchFeaturesLayer()


ROHBERG_BLUECHURCH_FEATURES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ROHBERG_BLUECHURCH_FEATURES_FIXTURE,),
    name='RohbergBluechurchFeaturesLayer:IntegrationTesting'
)


ROHBERG_BLUECHURCH_FEATURES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(ROHBERG_BLUECHURCH_FEATURES_FIXTURE,),
    name='RohbergBluechurchFeaturesLayer:FunctionalTesting'
)


ROHBERG_BLUECHURCH_FEATURES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        ROHBERG_BLUECHURCH_FEATURES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='RohbergBluechurchFeaturesLayer:AcceptanceTesting'
)

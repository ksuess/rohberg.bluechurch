# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s rohberg.bluechurch.features -t test_bluechurchprofile.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src rohberg.bluechurch.features.testing.ROHBERG_BLUECHURCH_FEATURES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_bluechurchprofile.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a bluechurchprofile
  Given a logged-in site administrator
    and an add bluechurchprofile form
   When I type 'My BluechurchProfile' into the title field
    and I submit the form
   Then a bluechurchprofile with the title 'My BluechurchProfile' has been created

Scenario: As a site administrator I can view a bluechurchprofile
  Given a logged-in site administrator
    and a bluechurchprofile 'My BluechurchProfile'
   When I go to the bluechurchprofile view
   Then I can see the bluechurchprofile title 'My BluechurchProfile'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add bluechurchprofile form
  Go To  ${PLONE_URL}/++add++bluechurchprofile

a bluechurchprofile 'My BluechurchProfile'
  Create content  type=bluechurchprofile  id=my-bluechurchprofile  title=My BluechurchProfile


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IDublinCore.title  ${title}

I submit the form
  Click Button  Save

I go to the bluechurchprofile view
  Go To  ${PLONE_URL}/my-bluechurchprofile
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a bluechurchprofile with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the bluechurchprofile title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

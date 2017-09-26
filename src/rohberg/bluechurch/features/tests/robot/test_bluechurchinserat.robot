# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s rohberg.bluechurch.features -t test_bluechurchinserat.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src rohberg.bluechurch.features.testing.ROHBERG_BLUECHURCH_FEATURES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_bluechurchinserat.robot
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

Scenario: As a site administrator I can add a BluechurchInserat
  Given a logged-in site administrator
    and an add bluechurchinserat form
   When I type 'My BluechurchInserat' into the title field
    and I submit the form
   Then a bluechurchinserat with the title 'My BluechurchInserat' has been created

Scenario: As a site administrator I can view a BluechurchInserat
  Given a logged-in site administrator
    and a bluechurchinserat 'My BluechurchInserat'
   When I go to the bluechurchinserat view
   Then I can see the bluechurchinserat title 'My BluechurchInserat'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add bluechurchinserat form
  Go To  ${PLONE_URL}/++add++BluechurchInserat

a bluechurchinserat 'My BluechurchInserat'
  Create content  type=BluechurchInserat  id=my-bluechurchinserat  title=My BluechurchInserat


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the bluechurchinserat view
  Go To  ${PLONE_URL}/my-bluechurchinserat
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a bluechurchinserat with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the bluechurchinserat title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s rohberg.bluechurch.features -t test_inserat.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src rohberg.bluechurch.features.testing.ROHBERG_BLUECHURCH_FEATURES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_inserat.robot
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

Scenario: As a site administrator I can add a Inserat
  Given a logged-in site administrator
    and an add inserat form
   When I type 'My Inserat' into the title field
    and I submit the form
   Then a inserat with the title 'My Inserat' has been created

Scenario: As a site administrator I can view a Inserat
  Given a logged-in site administrator
    and a inserat 'My Inserat'
   When I go to the inserat view
   Then I can see the inserat title 'My Inserat'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add inserat form
  Go To  ${PLONE_URL}/++add++Inserat

a inserat 'My Inserat'
  Create content  type=Inserat  id=my-inserat  title=My Inserat


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the inserat view
  Go To  ${PLONE_URL}/my-inserat
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a inserat with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the inserat title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

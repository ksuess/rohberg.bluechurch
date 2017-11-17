from plone import api
from rohberg.bluechurch.browser.views import back_references

def notifyEventAfterLocationChange(obj, event):
    """
    reindexObject(idxs=['modified'])
    """
    
    events = back_references(obj, "eventlocation")
    for ev in events:
        ev.reindexObject(idxs=['eventcity'])
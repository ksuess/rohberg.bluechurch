from zope import schema
from plone.supermodel import model
from dexterity.membrane.content.member import IMember
from rohberg.bluechurch.features import _

class IBluechurchmembraneprofile(IMember):
    """
    Artist or Event Manager
    """
    model.load('bluechurchmembraneprofile.xml')
    
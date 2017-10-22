# TODO: IBluechurchmembraneprofile mit Schema
# siehe dexterity.membrane.content.member.IMember

from dexterity.membrane.content.member import IMember

class IBluechurchmembraneprofile(IMember):
    """
    Artist or Event Manager
    TODO: Username automatisch konstruieren aus Vor- und Nachname
    """

    username = schema.ASCIILine(
        title=_(u"Username"),
        description=_(u"Enter a user name, usually something like 'jsmith'."
            " No spaces or special characters. Usernames and passwords are "
            "case sensitive, make sure the caps lock key is not enabled. "
            "This is the name used to log in.")
        required=True,
    )
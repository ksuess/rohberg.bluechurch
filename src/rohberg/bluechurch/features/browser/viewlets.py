from plone.app.layout.viewlets import common as base

class UserActionsViewlet(base.ViewletBase):
    """ Become a member

    """

    def isMember(self):
        """ TODO: isMember
        """
        return True
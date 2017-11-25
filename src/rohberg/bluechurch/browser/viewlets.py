from plone.app.layout.viewlets import common as base
from plone import api
from plone.app.content.interfaces import INameFromTitle


class UserActionsViewlet(base.ViewletBase):
    """ Become a member

    """

    def isMember(self):
        """ TODO: isMember
        """
        return True
        


class SnippetsViewlet(base.ViewletBase):
    """ diverse Snippets

    """
    @property
    def current_user(self):
        result = {}
        
        current = api.user.get_current()
        current_profile = api.content.get(UID=current.id)
        result['url'] = current_profile and current_profile.absolute_url() or "#"
        result['fullname'] = INameFromTitle(current_profile).title
        return result
        
    @property
    def can_edit(self):
        current = api.user.get_current()
        local_roles = api.user.get_roles(user=current, obj=self.context, inherit=False)
        return "Editor" in local_roles
from plone.app.layout.viewlets import common as base
from plone import api
from plone.app.content.interfaces import INameFromTitle


class BaseViewlet(base.ViewletBase):
    """ 
    """
    @property
    def current_user(self):
        result = {}
        
        current = api.user.get_current()
        current_profile = api.content.get(UID=current.id)
        result['url'] = current_profile and current_profile.absolute_url() or "#"
        result['fullname'] = current_profile and INameFromTitle(current_profile).title or u""
        return result
        
    @property
    def can_edit(self):
        current = api.user.get_current()
        local_roles = api.user.get_roles(user=current, obj=self.context, inherit=False)
        return "Editor" in local_roles or "Owner" in local_roles


class MemberActionsViewlet(BaseViewlet):
    """"""
    

class UserActionsViewlet(BaseViewlet):
    """"""
    
    def useractions(self):
        return []
    
    
class DocactionsViewlet(BaseViewlet):
    """
    
    """
    
    
class SnippetsViewlet(BaseViewlet):
    """ diverse Snippets

    """

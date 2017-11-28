from plone.memoize.view import memoize, memoize_contextless
from plone.app.layout.viewlets import common as base
from plone import api
from plone.app.content.interfaces import INameFromTitle
from plone.app.content.browser.folderfactories import _allowedTypes
from Products.CMFPlone.interfaces.constrains import IConstrainTypes
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

import logging
logger = logging.getLogger(__name__)


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
        
    # @property
    def can_edit(self):
        current = api.user.get_current()
        local_roles = api.user.get_roles(user=current, obj=self.context, inherit=True)
        return u"Editor" in local_roles or u"Owner" in local_roles
        
    # @property
    def can_add(self):
        current = api.user.get_current()
        local_roles = api.user.get_roles(user=current, obj=self.context, inherit=True)
        return u"Contributor" in local_roles

    
    @memoize
    def _locallyAllowedTypes(self):
        addContext = self.context

        allowed_types = _allowedTypes(self.request, addContext)
        constrain = IConstrainTypes(addContext, None)
        if constrain is None:
            return allowed_types
        locallyAllowed = constrain.getLocallyAllowedTypes()
        # logger.info("locallyAllowed: {}".format(locallyAllowed))
        return locallyAllowed
        
    # @property
    def can_add_here(self, type):
        context = self.context
        
        locallyAllowed = self._locallyAllowedTypes()
        
        current = api.user.get_current()
        local_roles = api.user.get_roles(user=current, obj=context, inherit=True)
        return (u"Contributor" in local_roles) and type in locallyAllowed


class MemberActionsViewlet(BaseViewlet):
    """"""
    

class UserActionsViewlet(BaseViewlet):
    """"""
    
    def useractions(self):
        return []
    
    
class DocactionsViewlet(BaseViewlet):
    """
    tal:condition="context/isPrincipiaFolderish"
    """
    
    
class SnippetsViewlet(BaseViewlet):
    """ diverse Snippets

    """

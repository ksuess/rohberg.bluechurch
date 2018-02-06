from plone.memoize.view import memoize, memoize_contextless
from plone.app.layout.viewlets import common as base
from plone import api
from plone.app.content.interfaces import INameFromTitle
from plone.app.content.browser.folderfactories import _allowedTypes
from Products.CMFCore.interfaces import IFolderish
from plone.app.contenttypes.interfaces import ICollection
from Products.CMFPlone.interfaces.constrains import IConstrainTypes
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

import logging
logger = logging.getLogger(__name__)


class BaseViewlet(base.ViewletBase):
    """ 
    """
    # TODO: cache per request
    @property
    @memoize_contextless
    def current_user(self):
        result = {}        
        current = api.user.get_current()
        current_profile = api.content.get(UID=current.id)
        result['id'] = current.id
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

    
    # @memoize
    def _locallyAllowedTypes(self, addContext):
        addContext = addContext or self.context

        allowed_types = _allowedTypes(self.request, addContext)
        constrain = IConstrainTypes(addContext, None)
        if constrain is None:
            return allowed_types
        locallyAllowed = constrain.getLocallyAllowedTypes()
        # logger.info("locallyAllowed: {}".format(locallyAllowed))
        return locallyAllowed
        
    @property
    def add_to_parent(self):
        return ICollection.providedBy(self.context)
    
    # @property
    # @memoize
    def can_add_here(self, type):
        context = self.context

        addContext = self.add_to_parent and context.aq_parent or context
        locallyAllowed = self._locallyAllowedTypes(addContext)
        
        current = api.user.get_current()
        local_roles = api.user.get_roles(user=current, obj=addContext, inherit=True)
        
        # logger.info(u"self.context {}, type {}".format(context, type))
        # logger.info(u"local_roles {}".format(local_roles))
        # logger.info(u"_locallyAllowedTypes {}".format(locallyAllowed))
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

class BacklinkViewlet(base.ViewletBase):
    """
    """
    
    def show(self):
        context = self.context
        pt = context.portal_type
        context_state = context.restrictedTraverse('@@plone_context_state')
        # print(context)
        # print(pt)
        # print(not pt in ["Folder", "Collection"])
        # # print(context_state)
        # print(context_state.is_default_page())
        # print(not context_state.is_default_page())
        result = not pt in ["Folder", "Collection"] and not context_state.is_default_page()
        return result
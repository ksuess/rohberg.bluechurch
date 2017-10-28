from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.browser.view import DefaultView
from Products.CMFCore.utils  import getToolByName

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch.features import _

class BluechurchmembraneprofileView(DefaultView):
    """ the default view for BluechurchProfile"""

    # def allbctags(self):
    #     bctags = queryUtility(IVocabularyFactory, name='rohberg.bluechurch.features.BluchurchTags')
    #     # import pdb; pdb.set_trace()
    #     result = bctags()(self.context).__dict__
    #     return result
    
    


class TestView(BrowserView):
    """ Testing utilities"""
    
    def wanttoknow(self):
        
        # from dexterity.membrane.content.member import IMember
        # from collective.dexteritytextindexer.utils import searchable
        #
        # searchable(IMember, 'first_name')
        # searchable(IMember, 'last_name')
        # searchable(IMember, 'bio')
        
        is_manager = api.user.has_permission('Manage portal')
        if is_manager:
            return "I am Manager"
        current = api.user.get_current()
        if api.user.is_anonymous():
            return "no Plone user logged in"
        user = current
        logger.info(user)
        username = user.getName()
        roles = api.user.get_roles(username=username)
        
        fullname = user.getProperty('fullname')
        email = user.getProperty('email')
        home_page = user.getProperty('home_page')
        
        pm = getToolByName(self.context, 'portal_membership')
        roles_in_context = pm.getAuthenticatedMember().getRolesInContext(self.context)
        return roles_in_context

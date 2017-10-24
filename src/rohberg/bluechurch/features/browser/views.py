from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.browser.view import DefaultView

from rohberg.bluechurch.features import _

class BluechurchprofileView(DefaultView):
    """ the default view for BluechurchProfile"""

    # def allbctags(self):
    #     bctags = queryUtility(IVocabularyFactory, name='rohberg.bluechurch.features.BluchurchTags')
    #     # import pdb; pdb.set_trace()
    #     result = bctags()(self.context).__dict__
    #     return result


class TestView(BrowserView):
    """ Testing utilities"""
    
    def wanttoknow(self):
        is_manager = api.user.has_permission('Manage portal')
        if is_manager:
            return "I am Manager"
        current = api.user.get_current()
        user = current
        username = user.getName()
        roles = api.user.get_roles(username=username)
        fullname = user.getProperty('fullname')
        email = user.getProperty('email')
        home_page = user.getProperty('home_page')
        return email

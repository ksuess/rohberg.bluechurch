from Acquisition import aq_inner
from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory

from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.browser.view import DefaultView
from plone.app.content.interfaces import INameFromTitle
from Products.CMFCore.utils  import getToolByName

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _


from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

def back_references(source_object, attribute_name):
    """
    Return back references from source object on specified attribute_name
    """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    rels = catalog.findRelations(
                dict(to_id=intids.getId(aq_inner(source_object)),
                from_attribute=attribute_name)
            )
    for rel in rels:
        try:
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        except KeyError, e:
            logger.error(str(e))
    return result
        
class BluechurchmembraneprofileView(DefaultView):
    """ the default view for BluechurchProfile"""

    # def allbctags(self):
    #     bctags = queryUtility(IVocabularyFactory, name='rohberg.bluechurch.BluchurchTags')
    #     # import pdb; pdb.set_trace()
    #     result = bctags()(self.context).__dict__
    #     return result
    
    
    def events(self):
        obs = back_references(self.context, "kontaktperson")
        result = []
        for obj in obs:
            if obj.portal_type=="bluechurchevent":
                result.append(obj)
        return result
        
    def locations(self):
        obs = back_references(self.context, "kontaktperson")
        result = []
        for obj in obs:
            if obj.portal_type=="bluechurchlocation":
                result.append(obj)
        return result     
           
    def inserate(self):
        obs = back_references(self.context, "kontaktperson")
        result = []
        for obj in obs:
            if obj.portal_type=="bluechurchinserat":
                result.append(obj)
        return result

    

class OwnedView(DefaultView):
    """
    """
    
    @property
    def kontaktperson_profile(self):
        kp = api.content.get(UID=self.context.kontaktperson.to_object.UID())
        return kp
        
    @property
    def kontaktperson_fullname(self):
        profile = self.kontaktperson_profile
        name_title = INameFromTitle(profile)
        return name_title.title
        

class BluechurchlocationView(OwnedView):
    """
    """        
    
    def events(self):
        obs = back_references(self.context, "location")
        result = []
        for obj in obs:
            if obj.portal_type=="bluechurchevent":
                result.append(obj)
        return result
    
class BluechurcheventView(OwnedView):
    """
    """
    
    @property
    def location_obj(self):
        obj = api.content.get(UID=self.context.location.to_object.UID())
        return obj
    
    @property
    def location_title(self):
        return self.location_obj.Title()


class BluechurchinseratView(OwnedView):
    """
    """    


class MyProfileView(BrowserView):
    """Gehe zu meinem Profile"""
    
    def __call__(self):
        current = api.user.get_current()
        profile = api.content.get(UID=current.id)
        response = self.request.response
        response.redirect(profile.absolute_url(), status=301)
        
    
class TestView(BrowserView):
    """ Testing utilities"""
    
    def wanttoknow(self):
        
        # from dexterity.membrane.content.member import IMember
        # from collective.dexteritytextindexer.utils import searchable
        #
        # searchable(IMember, 'first_name')
        # searchable(IMember, 'last_name')
        # searchable(IMember, 'bio')
        
        skinname = getSite().getCurrentSkinName()
        return skinname
        
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

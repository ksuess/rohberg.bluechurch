# coding: utf-8
from smtplib import SMTPException, SMTPRecipientsRefused
from Acquisition import aq_inner
from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory

from plone.memoize.view import memoize
from plone import api
from Products.CMFPlone.resources import add_resource_on_request
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.dexterity.browser.view import DefaultView
from plone.app.content.interfaces import INameFromTitle
from Products.CMFCore.utils  import getToolByName

from dexterity.membrane.behavior.user import INameFromFullName

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
    
    def __call__(self):
        add_resource_on_request(self.request, 'bluechurch_profile_features')
        return super(BluechurchmembraneprofileView, self).__call__()

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
           
    def starringat(self):
        obs = back_references(self.context, "beteiligte")
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
        
    @property
    def title(self):
        context = self.context
        ttl = INameFromFullName(context).title
        return ttl


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

    def __call__(self):
        # add_resource_on_request(self.request, 'bluechurch-locationsearch')
        return super(BluechurchlocationView, self).__call__()
    
    def events(self):
        obs = back_references(self.context, "eventlocation")
        result = []
        for obj in obs:
            if obj.portal_type=="bluechurchevent":
                result.append(obj)
        return result
    
class BluechurcheventView(OwnedView):
    """
    """
    
    @property
    @memoize
    def location_obj(self):
        obj = self.context.eventlocation.to_object
        # logger.info("location_obj geholt")
        return obj
    
    @property
    def location_title(self):
        return self.location_obj.Title()
    
    def beteiligte(self):
        profiles = [rel.to_object for rel in self.context.beteiligte]
        result = [{'fullname':INameFromTitle(profile).title, 'url':profile.absolute_url()} for profile in profiles]
        return result
        
    # def city(self):
    #     logger.info("BluechurcheventView def city")
    #     context = self.context
    #     event = context.portal_catalog(id=context.id)
    #     return event[0]['eventcity']


class BluechurchinseratView(OwnedView):
    """
    """    
    
class BluechurchpageView(OwnedView):
    """
    """    


class MyProfileView(BrowserView):
    """Gehe zu meinem Profil"""
    
    def __call__(self):
        current = api.user.get_current()
        profile = api.content.get(UID=current.id)
        response = self.request.response
        response.redirect(profile.absolute_url()) # , status=301


def sendMail(sender, recipient, subject, text, REQUEST):
    """ TODO: send Mail
    https://docs.plone.org/develop/plone/misc/email.html#sending-email
    
    sender, recipient:  type IBluechurchmembraneprofile
    """
    
    portal = api.portal.get()
    email_charset = 'UTF-8'
    mail_template = getMultiAdapter((portal, REQUEST), name="mail_template_bluechurch_en")
    mail_text = mail_template(sender=sender,
        recipient = recipient,
        messagetext=text,
        messagesubject=subject,
        portal_url=portal.absolute_url(),
        charset=email_charset,
        request=REQUEST)
    try:
        mail_host = api.portal.get_tool(name='MailHost')
        # The ``immediate`` parameter causes an email to be sent immediately
        # (if any error is raised) rather than sent at the transaction
        # boundary or queued for later delivery.
        if isinstance(mail_text, unicode):
            logger.info("unicode encoded")
            mail_text = mail_text.encode(email_charset)
        msgid = mail_host.send(mail_text, immediate=True)
    except SMTPRecipientsRefused:
        # Don't disclose email address on failure
        logger.error('Recipient address {} rejected by server'.format(recipient.email))
        # raise SMTPRecipientsRefused('Recipient address rejected by server')
    except Exception, e:
        logger.error(u"Unknown Exception sending mail.")
        # logger.error(u"Unknown Exception sending mail. {}".format(e))
    # logger.info(u"Bluechurch Message '{}' has been sent to {} {}".format(subject, recipient.id, recipient.email))




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
        
        is_manager = api.user.has_permission('Manage portal')
        if is_manager:
            return "I am Manager"
        current = api.user.get_current()
        if api.user.is_anonymous():
            return "no Plone user logged in"
        user = current
        logger.info(user)
        username = user.getName()
        roles = api.user.get_roles()
        permissions = api.user.get_permissions()
        
        fullname = user.getProperty('fullname')
        email = user.getProperty('email')
        home_page = user.getProperty('home_page')
        
        pm = getToolByName(self.context, 'portal_membership')
        roles_in_context = pm.getAuthenticatedMember().getRolesInContext(self.context)
        
        # return permissions
        return roles
        return roles_in_context
        return skinname



class FView(DefaultView):
    """Show all values of all fields
    
    """
    
    def wanttoknow(self):
        return "wanttoknow"
    

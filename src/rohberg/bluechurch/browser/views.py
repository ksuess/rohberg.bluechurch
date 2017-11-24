from Acquisition import aq_inner
from zope.component.hooks import getSite
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory

from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
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
    def location_obj(self):
        # obj = api.content.get(UID=self.context.eventlocation.to_object.UID())
        obj = self.context.eventlocation.to_object
        logger.info("location_obj geholt")
        return obj
    
    @property
    def location_title(self):
        return self.location_obj.Title()
    
    def beteiligte(self):
        profiles = [rel.to_object for rel in self.context.beteiligte]
        result = [{'fullname':INameFromTitle(profile).title, 'url':profile.absolute_url()} for profile in profiles]
        return result
        
    def city(self):
        context = self.context
        event = context.portal_catalog(id=context.id)
        return event[0]['eventcity']


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
    # mail_template = portal.mail_template_bluechurch_en # geht das?
    mail_template = getMultiAdapter((portal, REQUEST), name="mail_template_bluechurch_en")
    # mail_template = portal.restrictedTraverse("mail_template_bluechurch_en")
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
            mail_text = mail_text.encode(email_charset)
        return mail_host.send(mail_text, immediate=True)
    except SMTPRecipientsRefused:
        # Don't disclose email address on failure
        raise SMTPRecipientsRefused('Recipient address rejected by server')
    logger.info(u"Bluechurch Message '{}' sent to {}".format(subject, recipient))
            
class ContactBluechurchmember(BrowserView):
    """contact_bluechurchmember
    """
    
    def __call__(self):
        response = self.request.response
        request = self.request
        context = self.context
        current = api.user.get_current()
        current_profile = api.content.get(UID=current.id)
        if not current_profile:
            response.redirect(self.context.absolute_url())
            return
        recipient = self.context
        sender = current_profile
        subject = request.form.get("messagesubject", "").decode('utf-8')
        text = request.form.get("messagetext", "").decode('utf-8')
        messages = IStatusMessage(request)
        try:
            sendMail(sender, recipient, subject, text, request)
            messages.add(_(u"Message '{}' sent to {}.".format(subject, recipient.email)), type=u"info")
        except Exception, e:
            msg = _(u"Message '{}' not sent to {}. There were errors.".format(subject, recipient.email))
            logger.error(msg)
            logger.error(str(e))
            messages.add(msg, type=u"error")
            raise e
        response.redirect(context.absolute_url())

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



class FView(DefaultView):
    """Show all values of all fields
    
    """
    
    def wanttoknow(self):
        return "wanttoknow"
    

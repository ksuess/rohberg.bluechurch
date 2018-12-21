# coding: utf-8
from Acquisition import aq_inner
from collective.address.vocabulary import get_pycountry_name
from DateTime import DateTime
from dexterity.membrane.behavior.user import INameFromFullName
import os
from plone.memoize.view import memoize
from plone import api
from plone.dexterity.browser.view import DefaultView
from plone.app.content.interfaces import INameFromTitle
from Products.CMFPlone.resources import add_resource_on_request
from Products.CMFPlone import utils
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils  import getToolByName
from random import randint
from smtplib import SMTPException, SMTPRecipientsRefused
from zExceptions import BadRequest
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory
from zope.publisher.interfaces import IPublishTraverse

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


class Utilities(object):
    """Verschiedene utilities."""

    def get_commenter_home_url(self, username=None):
        if not username:
            return None
        profile = api.content.get(UID=username)
        if profile:
            return profile.absolute_url()

    def get_commenter_portrait(self, username=None):
        if not username:
            return None
        return self.get_commenter_home_url(username=username)+'/@@images/image/thumb'


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


    @memoize
    def back_references(self):
        brs = back_references(self.context, "kontaktperson")
        return brs

    @memoize
    def events(self):
        result = []
        today = DateTime()
        for obj in self.back_references():
            if obj.portal_type=="bluechurchevent":
                if DateTime(obj.end) >= today:
                    result.append(obj)
        result = sorted(result, key=lambda event: event.start)
        return result


    def locations(self):
        result = []
        for obj in self.back_references():
            if obj.portal_type=="bluechurchlocation":
                result.append(obj)
        return result

    def inserate(self):
        result = []
        for obj in self.back_references():
            if obj.portal_type=="bluechurchinserat":
                result.append(obj)
        return result

    def research(self):
        result = []
        for obj in self.back_references():
            if obj.portal_type=="bluechurchpage":
                result.append(obj)
        return result

    @property
    @memoize
    def title(self):
        context = self.context
        ttl = INameFromFullName(context).title
        # print(u"profile title {}".format(ttl))
        return ttl

    @property
    @memoize
    def is_current(self):
        context = self.context
        current = api.user.get_current()
        current_profile = api.content.get(UID=current.id)
        if not current_profile: # admin
            return False
        return context.id == current_profile.id


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
        # add_resource_on_request(self.request, 'bluechurch-locationsearch') # TODO später: add_bundle....
        return super(BluechurchlocationView, self).__call__()


class BluechurcheventView(OwnedView):
    """
    """

    def formatted_date(self, occ):
        provider = getMultiAdapter(
            (self.context, self.request, self),
            IContentProvider, name='formatted_date'
        )
        return provider(occ)

    def start(self):
        localized = api.portal.get_localized_time(datetime=self.context.start, long_format=True)
        return localized


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



from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

@implementer(IPublishTraverse)
class BackgroundView(BrowserView):
    """ Helpers

    call with /@@background/big
    or
    /@@background/small
    """

    def publishTraverse(self, request, size="big"):
        if size not in ('big', 'small'):
            raise BadRequest
        self.size = size
        return self

    def background(self, size="big"):
        num = randint(1, 17)
        path = os.path.dirname(__file__)
        if size == "small":
            filename = "theme/images/backgrounds_small/blue_church_"+str(num)+"_resized.jpg"
        else:
            filename = "theme/images/backgrounds/blue_church_"+str(num)+".jpg"
        self.filename = "/".join([path, "..", filename])
        f = open(self.filename, "rb")
        image_data = f.read()
        f.close()
        self.request.response.setHeader("Content-type", "image/jpeg")
        return image_data


    def __call__(self):
        bg = self.background(self.size)
        return bg



class TestView(BrowserView):
    """ Testing utilities"""

    def wanttoknow(self):
        context = self.context
        portal = api.portal


        items = context.portal_catalog(portal_type=['File', 'Image', 'BluechurchLocation', 'dexterity.membrane.bluechurchmembraneprofile'])
        for item in items[:100000]:
          obj = item.getObject()
          size = 0
          if obj.portal_type == 'File':
            size = obj.file.size
          else:
              field = obj.image
              if field:
                  size = field.size
          if size > 1024*1024 *1:
              url = u"<a href='{0}'>{0}</a>".format(item.getURL())
              print(u"***** {:.1f} {} {}".format(float(size)/1024/1024, url, obj.portal_type))

        return "sizes"


        for item in context.getFolderContents():
            name = INameFromFullName(item.getObject(), None)
            print(u"{:30} \t {:30} \t {:30} \t {:30}".format(item.portal_type, item.id, item.Title, name and name.title ))
        return context.id


        name = INameFromFullName(context, None)
        print(name)
        print(name.title)
        print(context.Title())
        return "INameFromFullName"

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

class UpdatePofileTypes(BrowserView):
    """"""

    def __call__(self):
        context = self.context
        print("*** update types")
        for ob in context.values():
            if ob.portal_type == "dexterity.membrane.bluechurchmembraneprofile":
                tt = ob.profile_type
                if not isinstance(tt, set):
                    print("{} {}".format(ob.id, tt))
                    # ob.profile_type = set([tt])
                    # ob.reindexObject()
            else:
                print(ob.portal_type)
        print("update done.")
        # for ob in context.values():
        #     print(ob.profile_type)

        # response = self.request.response
        # response.redirect(context.absolute_url()) # , status=301


class ListMembersInfo(BrowserView):

        def __call__(self):
            context = self.context
            portal_catalog = api.portal.get_tool('portal_catalog')
            items = portal_catalog(portal_type=['dexterity.membrane.bluechurchmembraneprofile', ])

            print("")
            for item in items:
              obj = item.getObject()
              print(u"{},{},{},{}".format(obj.email, obj.last_name, obj.first_name, get_pycountry_name(obj.country)))

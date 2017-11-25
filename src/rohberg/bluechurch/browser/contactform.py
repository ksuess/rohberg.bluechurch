# coding: utf-8
# https://docs.plone.org/develop/addons/schema-driven-forms/creating-a-simple-form/index.html

from plone.autoform.form import AutoExtensibleForm
from zope import interface
from zope import schema
from zope import component
from z3c.form import form, button

from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.content.interfaces import INameFromTitle

from rohberg.bluechurch.browser.views import sendMail

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _


class ProfileContactFormSchema(interface.Interface):

    messagesubject = schema.TextLine(
            title=_(u"label_subject"),
            required=True,
        )

    messagetext = schema.Text(
            title=_(u"label_messagetext"),
            required=True,
        )
    # favorite = schema.TextLine(
    #         title=_(u"Favorite"),
    #         required=False,
    #     )
    # seaheight = schema.TextLine(
    #         title=_(u"Höhe über Meer"),
    #         required=False,
    #     )


class ProfileContactFormAdapter(object):
    interface.implements(ProfileContactFormSchema)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.messagesubject = None
        self.messagetext = None
        
        
class ProfileContactForm(AutoExtensibleForm, form.Form):
    schema = ProfileContactFormSchema
    form_name = 'contact_form'

    label = _(u"Contact an Artist or Event Manager") # TODO: name des Artists anzeigen
    # description = _(u"We will contact you to confirm your order and delivery.")
    description = _(u"The recipient gets an email with your email address to get back to you.")

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(ProfileContactForm, self).update()

    @button.buttonAndHandler(_(u'label_send'))
    def handleApply(self, action):
        logger.info("contact_bluechurchprofile")
        
        context = self.context

        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Handle order here. For now, just print it to the console. A more
        # realistic action would be to send the order to another system, send
        # an email, or similar

        fullname = INameFromTitle(context).title


        response = self.request.response
        request = self.request
        current = api.user.get_current()
        current_profile = api.content.get(UID=current.id)
        if not current_profile:
            response.redirect(self.context.absolute_url())
            return
        recipient = self.context
        sender = current_profile
        subject = data['messagesubject']
        # subject = subject or _(u"{} wants to contact you due to Jazz and Sermon stuff.".format(INameFromTitle(sender).title))
        # subject = subject.decode('utf-8')
        text = data['messagetext'] #.decode('utf-8')
        messages = IStatusMessage(request)
        try:
            sendMail(sender, recipient, subject, text, request)
            logger.info("contact_bluechurchprofile send.")
        except Exception, e:
            msg = _(u"Message '{}' not sent to {}. There were errors.".format(subject, recipient.email))
            logger.error(msg)
            logger.error(str(e))
            # messages.addStatusMessage(_(msg, "error"))
            raise e


        # Redirect back to the front page with a status message

        messages.addStatusMessage(
                _(u"Message '{}' sent to {}.".format(subject, fullname)),
                "info"
            )
        logger.info("jetzt redirect")
        # TODO: im Modal bleiben.
        contextURL = recipient.absolute_url()
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(u"label_cancel"))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
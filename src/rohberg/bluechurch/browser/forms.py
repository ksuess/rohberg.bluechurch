from Acquisition import aq_inner
from AccessControl import Unauthorized
from zope.component import getUtility
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.browser import add

import logging
logger = logging.getLogger(__name__)

from rohberg.bluechurch import _

class AddForm(add.DefaultAddForm):
    portal_type = 'dexterity.membrane.bluechurchmembraneprofile'
    
    def update(self):
        # TODO: Profile nur in Folder "profiles". cleanup restriction to folder profiles
        container = aq_inner(self.context)
        if container.id != "profiles":
            raise Unauthorized(_(u"No Profiles here. Change to 'Profiles'."))
            
        is_manager = api.user.has_permission('Manage portal')
        is_sitemanager = False
        if not(api.user.is_anonymous() or is_manager):
            current = api.user.get_current()
            user = current
            username = user.getName()
            roles = api.user.get_roles(username=username)
            is_sitemanager = "Site Administrator" in roles
            logger.info("roles and is_anonymous: {} {}".format(roles, is_sitemanager))
        if not(api.user.is_anonymous() or is_manager or is_sitemanager):
            raise Unauthorized(_(u"You are already registered."))
        # try:
        #     super(AddForm, self).update()
        # except ValueError, e:
        #     logger.warn("User tried to add Profile outside folder profile")
        super(AddForm, self).update()
        

    def add(self, object):
        """      
        """
        
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        new_object = addContentToContainer(container, object, checkConstraints=False)

        if fti.immediate_view:
            self.immediate_view = "/".join(
                [container.absolute_url(), new_object.id, fti.immediate_view]
            )
        else:
            self.immediate_view = "/".join(
                [container.absolute_url(), new_object.id]
            )



class AddView(add.DefaultAddView):
    form = AddForm
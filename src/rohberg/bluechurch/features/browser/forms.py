from Acquisition import aq_inner
from AccessControl import Unauthorized
from zope.component import getUtility
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.browser import add

class AddForm(add.DefaultAddForm):
    portal_type = 'dexterity.membrane.bluechurchmembraneprofile'
    
    def update(self):
        # TODO: check here if the user is anonymous and raise exception if not
        is_manager = api.user.has_permission('Manage portal')
        is_sitemanager = False
        if not(api.user.is_anonymous() or is_manager):
            current = api.user.get_current()
            user = current
            username = user.getName()
            roles = api.user.get_roles(username=username)
            is_sitemanager = "Site Administrator" in roles
        if not(api.user.is_anonymous() or is_manager or is_sitemanager):
            raise Unauthorized('You are already registered.')
        super(AddForm, self).update()
        
        



    def add(self, object):
        """ TODO: Profile nur in Folder "profiles"
        
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
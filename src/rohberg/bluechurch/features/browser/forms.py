from Acquisition import aq_inner
from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.browser import add

class AddForm(add.DefaultAddForm):
    portal_type = 'dexterity.membrane.bluechurchmembraneprofile'
    
    def update(self):
        # TODO: check here if the user is anonymous and raise exception if not
        super(AddForm, self).update()

    def add(self, object):
        
        print("** add method of custom AddForm")
        
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
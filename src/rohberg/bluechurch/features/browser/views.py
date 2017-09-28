from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MyView(BrowserView):

    # index = ViewPageTemplateFile("my-template.pt")

    # def render(self):
    #     return self.index()

    def __call__(self):
        # return self.render()
        bctags = queryUtility(IVocabularyFactory, name='rohberg.bluechurch.features.BluchurchTags')
        # import pdb; pdb.set_trace()
        result = bctags()(self.context).__dict__
        return result


# coding: utf-8
from AccessControl import getSecurityManager
from plone import api
from plone.namedfile.interfaces import INamedBlobImageField
from plone.namedfile.interfaces import INamedBlobFileField
# from plone.app.contenttypes.interfaces import IImage
from zope.interface import Invalid
from z3c.form import validator


from rohberg.bluechurch import _

class FileFileSizeValidator(validator.FileUploadValidator):

    def validate(self, value):
        super(FileFileSizeValidator, self).validate(value)

        portal = api.portal.get()
        
        # if Site Manager: no limit
        sm = getSecurityManager()
        if sm.checkPermission('Add portal member', portal):
            pass
        else:
            maximumSize = api.portal.get_registry_record('rohberg.bluechurch.maxFileSize')           
            msgid = _(u"file_too_large_msg", default=u"File is too large (more than ${result} MB)", 
                mapping={u"result": "{:.1f}".format(float(maximumSize)/1000)})
            translated = self.context.translate(msgid)            
            if value.getSize() > maximumSize*1000:
                raise Invalid(translated)


class ImageFileSizeValidator(validator.FileUploadValidator):

    def validate(self, value):
        super(ImageFileSizeValidator, self).validate(value)
        portal = api.portal.get()
        
        # if Site Manager: no limit
        sm = getSecurityManager()
        if sm.checkPermission('Add portal member', portal):
            pass
        else: 
            maximumSize = api.portal.get_registry_record('rohberg.bluechurch.maxImageSize')            
            msgid = _(u"image_too_large_msg", default=u"Image is too large (more than ${result} MB)", 
                mapping={u"result": "{:.1f}".format(float(maximumSize)/1000)})
            translated = self.context.translate(msgid)            
            if value and value.getSize() > maximumSize*1000:
                raise Invalid(translated)


validator.WidgetValidatorDiscriminators(FileFileSizeValidator,
                                        field=INamedBlobFileField)

validator.WidgetValidatorDiscriminators(ImageFileSizeValidator,
                                        # context=IImage,
                                        field=INamedBlobImageField)
                                        





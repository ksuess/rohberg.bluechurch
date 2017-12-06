# -*- coding: utf-8 -*-

__import__('pkg_resources').declare_namespace(__name__)

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('rohberg.bluechurch')




from collective.address.behaviors import IAddress

IAddress['zip_code'].required = True
IAddress['city'].required = True
IAddress['country'].required = True
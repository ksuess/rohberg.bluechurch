# -*- coding: utf-8 -*-
from zope.component import adapter
from zope.interface import implementer

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone import api

from collective.collectionfilter.interfaces import IGroupByCriteria
from collective.collectionfilter.interfaces import IGroupByModifier

import logging
logger = logging.getLogger(__name__)

@implementer(IGroupByModifier)
@adapter(IGroupByCriteria)
def groupby_modifier(groupby):
    """ todo: collectionfilter display_modifier for country"""
    factory = getUtility(IVocabularyFactory, 'collective.address.CountryVocabulary')
    countryvocabulary = factory(api.portal.get())
    try:
        groupby._groupby['country']['display_modifier'] = lambda it: countryvocabulary.getTerm(it).title
    except KeyError as  e:
        logger.error(str(e))
    
    # groupby._groupby['Subject']['display_modifier'] = lambda x: x.upper()
    # groupby._groupby['my_new_index'] = {
    #     'index': 'my_new_index',
    #     'metadata': 'my_new_index_metadata_colum',
    #     'display_modifier': lambda it: u'this is awesome: {0}'.format(it)
    # }
    #
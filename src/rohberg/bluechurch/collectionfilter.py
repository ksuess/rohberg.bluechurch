# -*- coding: utf-8 -*-
from zope.component import adapter
from zope.interface import implementer

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone import api

from collective.collectionfilter.interfaces import IGroupByCriteria
from collective.collectionfilter.interfaces import IGroupByModifier


@implementer(IGroupByModifier)
@adapter(IGroupByCriteria)
def groupby_modifier(groupby):
    factory = getUtility(IVocabularyFactory, 'collective.address.CountryVocabulary')
    countryvocabulary = factory(api.portal.get())
    groupby._groupby['country']['display_modifier'] = lambda it: countryvocabulary.getTerm(it).title
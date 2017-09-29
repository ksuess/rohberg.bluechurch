# coding: utf-8

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

def BluchurchTagsVocabularyFactory(context=None):
    terms = []
    terms.append(SimpleVocabulary.createTerm("kinder", "kinder", u"Kinder"))
    terms.append(SimpleVocabulary.createTerm("madchen", "madchen", u"Mädchen"))
    terms.append(SimpleVocabulary.createTerm("senioren", "senioren", u"Senioren"))
    return SimpleVocabulary(terms)

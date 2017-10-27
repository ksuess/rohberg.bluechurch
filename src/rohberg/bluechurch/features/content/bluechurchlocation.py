# coding: utf-8
from zope.interface import implementer
from plone.dexterity.content import Item
from plone.supermodel import model
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from plone.autoform import directives

from rohberg.bluechurch.features import _

""" ALLOWED_FIELDS = [
    u'plone.app.textfield.RichText',
    u'plone.namedfile.field.NamedBlobImage',
    u'plone.namedfile.field.NamedBlobFile',
    u'plone.schema.email.Email',
    u'z3c.relationfield.schema.RelationChoice',
    u'z3c.relationfield.schema.RelationList',
    u'zope.schema._bootstrapfields.Bool',
    u'zope.schema._bootstrapfields.Int',
    u'zope.schema._bootstrapfields.Password',
    u'zope.schema._bootstrapfields.Text',
    u'zope.schema._bootstrapfields.TextLine',
    u'zope.schema._field.Choice',
    u'zope.schema._field.Date',
    u'zope.schema._field.Datetime',
    u'zope.schema._field.Float',
    u'zope.schema._field.Set',
    u'zope.schema._field.URI',
]
"""
class IBluechurchlocation(model.Schema):
    """ Marker interface for Bluechurchlocation
    """

    # # remove after debugging
    # read_permission(profilepy='zope2.View')
    # write_permission(profilepy='rohberg.bluechurch.addbluechurchcontent')
    # profilepy = RelationChoice(
    #     title=_(u"profilepy"),
    #     source=CatalogSource(portal_type=['dexterity.membrane.bluechurchmembraneprofile',]),
    #     required=False,
    # )

    # Kontaktperson
    read_permission(kontaktperson='zope2.View')
    write_permission(kontaktperson='rohberg.bluechurch.addbluechurchprofile')
    kontaktperson = RelationChoice(
        title=_(u"Kontaktperson"),
        source=CatalogSource(portal_type=['dexterity.membrane.bluechurchmembraneprofile',]),
        required=True,
    )


    # # remove after debugging
    # directives.widget('kontaktperson2', AutocompleteFieldWidget)
    # read_permission(kontaktperson2='zope2.View')
    # write_permission(kontaktperson2='rohberg.bluechurch.addbluechurchprofile')
    # kontaktperson2 = RelationChoice(
    #     title=_(u"kontaktperson2"),
    #     source=CatalogSource(portal_type=['dexterity.membrane.bluechurchmembraneprofile',]),
    #     required=True,
    # )
    
    
    # dokupy = RelationChoice(
    #     title=_(u"Referenziertes Objekt"),
    #     source=ObjPathSourceBinder(
    #         portal_type="Dokument",
    #         navigation_tree_query=dict(
    #             portal_type=["Dokument",],
    #             path={ "query": '/web/profiles' })
    #     ),
    #     required=False,
    # )
    
    model.load('bluechurchlocation.xml')


@implementer(IBluechurchlocation)
class Bluechurchlocation(Item):
    """
    """

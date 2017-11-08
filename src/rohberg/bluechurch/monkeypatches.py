from copy import deepcopy
from zope.schema.interfaces import IContextAwareDefaultFactory
from z3c.relationfield.interfaces import IRelationChoice

import logging
logger = logging.getLogger(__name__)

from plone.dexterity.content import _marker

def patched_default_from_schema(context, schema, fieldname):
    """helper to lookup default value of a field
    """
    if schema is None:
        return _marker
    field = schema.get(fieldname, None)
    if field is None:
        return _marker

    # logger.info(fieldname)
    # logger.info(schema)
    # logger.info(field)
    # import pdb; pdb.set_trace()
    if IContextAwareDefaultFactory.providedBy(
            getattr(field, 'defaultFactory', None)
    ):
        bound = field.bind(context)
        schnupsi = bound
    else:
        schnupsi = field
    if IRelationChoice.providedBy(schnupsi):
        return schnupsi.default
    else:
        return deepcopy(schnupsi.default)
    return _marker
    


def yypatched_default_from_schema(context, schema, fieldname):
    """helper to lookup default value of a field
    
    das Original
    """
    if schema is None:
        return _marker
    field = schema.get(fieldname, None)
    if field is None:
        return _marker
    if IContextAwareDefaultFactory.providedBy(
            getattr(field, 'defaultFactory', None)
    ):
        bound = field.bind(context)
        return deepcopy(bound.default)
    else:
        return deepcopy(field.default)
    return _marker
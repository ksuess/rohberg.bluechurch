# coding: utf-8
import re
from zope.schema import URI
from zope.schema.interfaces import InvalidURI

_hasprotocol = r"[a-zA-z0-9+.-]+://"
_hasprotocol += r"\S*$"  # non space
_hasprotocol = re.compile(_hasprotocol).match

_isuri = r"\S*\.\S*$"  # non space (should be pickier)
_isuri = re.compile(_isuri).match


class URI_bluechurch(URI):
    """ Validator: Kein Protokoll notwendig
    
    wenn kein Protokoll, dann http:// davorhängen
    """
    
    def _validate(self, value):
        super(URI, self)._validate(value)
        if _isuri(value):
            return

        raise InvalidURI(value)

    def fromUnicode(self, value):
        """ See IFromUnicode.
        """
        v = str(value.strip())
        self.validate(v)
        if not _hasprotocol(v):
            v = "http://" + v
        return v
    
# coding: utf-8

from plone import api
from zope.component.hooks import getSite
from plone.app.uuid.utils import uuidToPhysicalPath

def get_site_path(context=None):
    return u'/'.join(getSite().getPhysicalPath())
    

def get_profiles_base_path(context):
    search_base = api.portal.get_registry_record('rohberg.bluechurch.profiles_base')
    path = get_site_path(context)
    if search_base:
        # path = search_base
        path = uuidToPhysicalPath(search_base)
        print("path " + path)
    print("final path (get_profiles_base_path) " + path)
    return path
    

    #     ctx = getSite()
    #     if not IPloneSiteRoot.providedBy(ctx):
    #         ctx = aq_parent(ctx)
    # return u'/'.join(ctx.getPhysicalPath())

def get_locations_base_path(context):
    search_base = api.portal.get_registry_record('rohberg.bluechurch.locations_base')
    path = get_site_path(context)
    if search_base:
        # path = search_base
        path = uuidToPhysicalPath(search_base)
        print("path " + path)
    print("final path (get_locations_base_path) " + path)
    return path
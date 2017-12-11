from plone.memoize import view
from Products.CMFPlone.PloneBatch import Batch
from plone.app.querystring import queryparser
from plone.app.event.browser.event_listing import EventListing
from plone.app.event.base import RET_MODE_OBJECTS, RET_MODE_ACCESSORS
from plone.app.event.base import _prepare_range
from plone.app.event.base import start_end_query
from plone.app.event.base import expand_events
from plone.app.event.base import _obj_or_acc

import logging
logger = logging.getLogger(__name__)

class BluechurchEventListing(EventListing):
    """ Collection View
    
    Allgemeine View, nicht nur Events
    """

    def __init__(self, context, request):
        super(BluechurchEventListing, self).__init__(context, request)
        
        self.schnupsi = u"foo"
        

    # @view.memoize
    def events(self, ret_mode=RET_MODE_ACCESSORS, expand=True, batch=True):
        # logger.info("getting batch for event_listing")
        res = []
        if self.is_collection:
            ctx = self.default_context

            sort_on = ctx.sort_on
            sort_order = ctx.sort_reversed and "reverse" or ""
            ret_mode = RET_MODE_OBJECTS
            # logger.info("sort_order: {}".format(sort_order))
            
            query = queryparser.parseFormquery(
                ctx, ctx.query, sort_on=sort_on, sort_order=sort_order
            )

            custom_query = query
            custom_query.update(self.request.get('contentFilter', {}))
            # logger.info("events custom_query: {}".format(custom_query))

            if not 'start' in query and not 'end' in query:
                res = ctx.results(
                    batch=False, brains=True, custom_query=custom_query
                )
                res = [it.getObject() for it in res]
            else:
                res = ctx.results(
                    batch=False, brains=True, custom_query=custom_query
                )
                if expand:
                    # get start and end values from the query to ensure limited
                    # listing for occurrences
                    start, end = self._expand_events_start_end(
                        query.get('start') or custom_query.get('start'),
                        query.get('end') or custom_query.get('end')
                    )
                    res = expand_events(
                        res, ret_mode,
                        start=start, end=end,
                        sort=sort_on, sort_reverse=True if sort_order else False
                    )
        
                else:
                    res = self._get_events(ret_mode, expand=expand)
        # !CSRF!
        # for item in res:
        #     item.has_image = item.image and True or False
        if batch:
            b_start = self.b_start
            b_size = self.b_size
            res = Batch(res, size=b_size, start=b_start, orphan=self.orphan)

        # logger.info("FINAL results: {}".format(res))
        return res

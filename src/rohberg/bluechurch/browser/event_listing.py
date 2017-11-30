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
    """"""

    def __init__(self, context, request):
        super(BluechurchEventListing, self).__init__(context, request)
        
        self.schnupsi = u"foo"
        

    # @view.memoize
    def events(self, ret_mode=RET_MODE_ACCESSORS, expand=True, batch=True):
        res = []
        if self.is_collection:
            ctx = self.default_context

            # result = ctx.results(
            #     batch=False, brains=False, custom_query=ctx.query
            # )
            # res = [_obj_or_acc(it.getObject(), ret_mode) for it in result]
            # logger.info("res: {}".format(res))
            # logger.info("expand: {}".format(expand))
            # logger.info("contentFilter: {}".format(self.request.get('contentFilter', {})))
            
            
            # logger.info("expand: {}".format(expand))
            # logger.info("batch: {}".format(batch))
            # logger.info("ctx.query {}".format(ctx.query))
            # logger.info("contentFilter: {}".format(self.request.get('contentFilter', {})))
            
            # # Whatever sorting is defined, we're overriding it.
            # sort_on = 'start'
            # sort_order = None
            # if self.mode in ('past', 'all'):
            #     sort_order = 'reverse'
            sort_on = ctx.sort_on
            sort_order = ctx.sort_reversed and "reverse" or "ascending"
            ret_mode = RET_MODE_OBJECTS
            
            query = queryparser.parseFormquery(
                ctx, ctx.query, sort_on=sort_on, sort_order=sort_order
            )
            # logger.info("query: {}".format(query))
            # custom_query = self.request.get('contentFilter', {})
            # if 'start' not in query or 'end' not in query:
            #     # ... else don't show the navigation bar
            #     start, end = self._start_end
            #     start, end = _prepare_range(ctx, start, end)
            #     custom_query.update(start_end_query(start, end))
            custom_query = query
            custom_query.update(self.request.get('contentFilter', {}))
            res = ctx.results(
                batch=False, brains=True, custom_query=custom_query
            )
            # logger.info("events custom_query: {}".format(custom_query))
            # logger.info("results: {}".format(res))
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
            logger.info("expanded results: {}".format(res))
        else:
            res = self._get_events(ret_mode, expand=expand)
        if batch:
            b_start = self.b_start
            b_size = self.b_size
            res = Batch(res, size=b_size, start=b_start, orphan=self.orphan)
        return res

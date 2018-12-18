require.config({
  baseUrl: "++theme++bluechurch/js/",
  paths: {
      "pdfjs-dist": "pdfjs/",
  }
});

require([
  'jquery',
  'pdfjs-dist/pdf',
], function($, pj) {
    // now have access to jQuery (as $) and pdfjs (as pj), both defined as modules in the RequireJS configuration.
   'use strict';

   console.debug(pj);


});

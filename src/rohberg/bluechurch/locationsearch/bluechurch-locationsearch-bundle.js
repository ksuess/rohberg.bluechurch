require([
  'pat-registry',
  'bluechurch-locationsearch'
], function(registry) {
  'use strict';

  // initialize only if we are in top frame
  if (window.parent === window) {
    $(document).ready(function() {
      if (!registry.initialized) {
        registry.init();
      }
    });
  }

});
// TODO: dritte Zeile in require: checken
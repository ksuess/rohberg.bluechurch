



require([
    'jquery',
    'pat-base',
], function($, Base) {
    'use strict';

    var Pattern = Base.extend({
        name: 'rohberg-bluechurch-bcfeatures',
        trigger: '.pat-bcfeatures',
        parser: 'mockup',
        defaults: {
            // minHeight: 200,
            // minWidth: 200
        },
        init: function() {
            var that = this;
            that.$el.append(' <span>Blue Goast was here</span>');
            
            $(document).ready(function() {

  
                $( "#clickme_contact_bluechurchmember" ).click(function() {
                  $( "#contact_bluechurchmember form" ).slideToggle( "slow", function() {
                    // Animation complete.
                  });
                });
            }
        }
    });
    
    return Pattern;
});
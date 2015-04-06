'use strict';
define(['underscore', 'handlebars'], function(_, Handlebars) {
    var helpers = {
    	jsonify: function(objectRef) {
        	return JSON.stringify(objectRef, false, '    ');
        },
        stripScript: function(context) {
          var html = context;
              // context variable is the HTML you will pass into the helper
              // Strip the script tags from the html, and return it as a Handlebars.SafeString
              return new Handlebars.SafeString(html);
        }
    };
    return {
    	'helpers': helpers,
    	'register': function() {
    		_.each(helpers, function(helper, name) {
    			Handlebars.registerHelper(name, helper);
    		});
    	}
    };
});

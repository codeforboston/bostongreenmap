'use strict';
define(['underscore', 'handlebars'], function(_, Handlebars) {
    var helpers = {
    	jsonify: function(objectRef) {
        	return JSON.stringify(objectRef, false, '    ');
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

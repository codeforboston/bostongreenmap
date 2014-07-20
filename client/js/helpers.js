'use strict';
define(['underscore', 'handlebars'], function(_, Handlebars) {
    var helpers = {
    	jsonify: function(objectRef) {
        	return JSON.stringify(objectRef, false, '    ');
        },
        sectionIntoThrees: function(responses) {
          var countElements = 0;
          var icons = [{images: []}];
          responses.forEach(function(item) {
            if (countElements == 3) {
              icons.push({images: []});
              countElements = 0;
            }
            if (item.images) {
              icons[icons.length - 1]['images'].push({ src: images[0].src, caption: images[0].caption, name: item.name, link: item.url});
              countElements++;
            }
          });
          icons[0].activeClass = 'active';
          return icons;
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

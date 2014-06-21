'use strict';
define(['underscore', 'handlebars'], function(_, Handlebars) {
    var jsonify = function(objectRef) {
        return JSON.stringify(objectRef, false, '    ');
    }
    return {
    	'jsonify': jsonify
    };
});

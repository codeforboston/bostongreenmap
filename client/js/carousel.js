'use strict';
define(['underscore', 'backbone', 'marionette', 'build/templates', 'js/helpers'], function(_, Backbone, Marionette, templates, helpers) {
    var CarouselItemView = Marionette.ItemView.extend({
        template: templates['templates/recommendedImageCarousel.hbs'],
        initialize: function(parks) {
            this.parks = parks;
        },
        serializeData: function() {
            console.log('helpers', helpers);
            var parksInThrees = helpers.sectionIntoThrees();
            console.log('parksInThrees', parksInThrees);
            return {
                'parksInThrees': parksInThrees
            };
        }
    });

    return {
        CarouselItemView: CarouselItemView
    };
});
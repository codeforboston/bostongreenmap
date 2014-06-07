define(['backbone', 'marionette', 'build/templates'], function(Backbone, Marionette, templates) {
    var app = new Marionette.Application();
    app.addRegions({
        mainRegion: '#content-area'
    });

    var ParkLayout = Marionette.Layout.extend({
        template: templates['templates/ArticleLayout.hbs'],
        regions: {
            'navRegion': '#boston-green-navbar-container',
            'parkRegion': '#park-region'
        }
    });

    var Park = Backbone.Model.extend({
        defaults: {
            'title': ''
        }
    });

    var ParksCollection = Backbone.Collection.extend({
        model: Park,
        url: function() {
            return window.location.origin + '/parks/search?no_map=True&neighborhoods=25';
        },
        parse: function(response) {
            var parks = _.map(response.parks, function(park) {
                return new Park(park);
            });
            console.log('parks: ', parks);
            return parks;
        }
    });

    Park.Collection = ParksCollection;

    var ParkListItemView = Marionette.ItemView.extend({
        template: templates['templates/ArticleListItem.hbs'],
        tagName: 'li',
        className: 'article'
    });

    var ParkListView = Marionette.CompositeView.extend({
        template: templates['templates/ArticleList.hbs'],
        itemView: ParkListItemView,
        tagName: 'ul',
        className: 'article-list'
    });

    app.addInitializer(function(options) {
        var parks = new ParksCollection();
        parks.fetch({
            'dataType': 'json',
            'success': function(data) {
                var parkListView = new ParkListView({'collection': parks});

                var parkLayout = new ParkLayout();
                parkLayout.render();
                parkLayout.parkRegion.show(parkListView);
                app.getRegion('mainRegion').show(parkLayout);
                console.log(parkListView);
            }
        });
    });

    return {
        startModule: function(done) {
            app.start({});
        }
    };
});

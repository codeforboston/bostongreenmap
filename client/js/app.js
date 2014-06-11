define(['backbone', 'marionette', 'build/templates'], function(Backbone, Marionette, templates) {
    var app = new Marionette.Application();
    app.addRegions({
        navRegion: '#header',
        mainRegion: '#content-area',
        footerRegion: '#footer'
    });

    // Models
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
    
    // Views
    var HeaderView = Marionette.ItemView.extend({
        template: templates['templates/headerView.hbs'],
        tagName: 'div',
        className: 'header'
    });

    var SearchView = Marionette.ItemView.extend({
        template:templates['templates/search.hbs'],
        tagName: 'div',
        className: 'finder'
    });

    var FooterView = Marionette.ItemView.extend({
        template: templates['templates/footer.hbs'],
        tagName: 'div',
        className: 'footer'
    });

    // var ParkListItemView = Marionette.ItemView.extend({
    //     template: templates['templates/parkListItem.hbs'],
    //     tagName: 'li',
    //     className: 'article'
    // });

    // var ParkListView = Marionette.CompositeView.extend({
    //     template: templates['templates/parkList.hbs'],
    //     itemView: ParkListItemView,
    //     tagName: 'ul',
    //     className: 'article-list'
    // });

    // var ParkLayout = Marionette.Layout.extend({
    //     template: templates['templates/parkLayout.hbs'],
    //     regions: {
    //         'navRegion': '#boston-green-navbar-container',
    //         'parkRegion': '#park-region'
    //     }
    // });

    app.addInitializer(function(options) {
        var parks = new ParksCollection();
        // var parkLayout = new ParkLayout();
        app.getRegion('navRegion').show(new HeaderView());
        app.getRegion('mainRegion').show(new SearchView({'collection': parks}));
        app.getRegion('footerRegion').show(new FooterView());

        // parkLayout.render();
        // parks.fetch({
        //     'dataType': 'json',
        //     'success': function(data) {
        //         var parkListView = new ParkListView({'collection': parks});
        //         // parkLayout.parkRegion.show(parkListView);
        //         app.getRegion('mainRegion').show(parkListView);
        //     }
        // });
    });

    return {
        startModule: function(done) {
            app.start({});
        }
    };
});


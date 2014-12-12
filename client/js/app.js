define([
    'backbone',
    'marionette',
    'build/templates',
    'masonry',
    'bootstrap',
    'owl'
], function(
    Backbone,
    Marionette,
    templates,
    Masonry,
    owl
) {
    var app = new Marionette.Application(),
        router;

    app.addRegions({
        navRegion: '#header',
        mainRegion: '#content-area',
        footerRegion: '#footer'
    });


    // Models
    var Park = Backbone.Model.extend({
        initialize: function (params) {
          this.park_slug = params.park_slug
        },
        defaults: {
            'title': ''
        },
        url: function() {
            return window.location.origin + '/parks/search/?slug=' + this.park_slug;
        },
        parse: function (response) {
          var attributes = {};
          _.each(response, function(attribute, key) {
            _.each(attribute, function(attribute, key) {
              attributes[key] = attribute;
            })
          });
          return attributes;
        },
        render: function() {

        }
    });

    var SearchModel = Backbone.Model.extend({
        url: function() {
            return window.location.origin + '/parks/get_neighborhoods_and_activities_list/';
        },
        parse: function(response) {
            var data = {'neighborhoods': [], 'activities': [], 'featured_parks': []};
            _.each(response.neighborhoods, function(neighborhood) {
                data.neighborhoods.push({'id': neighborhood.id, 'name': neighborhood.name});
            });
            _.each(response.activities, function(activity) {
                data.activities.push({'id': activity.id, 'name': activity.name});
            });
            _.each(response.featured_parks, function(featured_park) {
                data.featured_parks.push({'id': featured_park.id, 'name': featured_park.name, 'url': featured_park.url });
            });
            return data;
        }
    });

    var ParksCollection = Backbone.Collection.extend({
        model: Park,
        initialize: function(params) {
            this.queryString = params.queryString
        },
        url: function() {
            var search_url = 'parks/search?' + this.queryString;
            return search_url;
        },
        parse: function(response) {
            if (!response) {
                alert('no data for that search!');
            }
            var parks = _.map(_.values(response.parks), function(park) {
                return new Park(park);
            });
            return parks;
        }
    });
    
    // Views
    var HeaderView = Marionette.ItemView.extend({
        events: {
            'click #nav-about': 'goToAbout',
            'click #nav-mission': 'goToMission',
            'click #nav-index': 'goToIndex',
            'click #nav-contact': 'goToContact'
        },
        template: templates['templates/header.hbs'],
        tagName: 'div',
        className: 'header',
        goToAbout: function(evt) {
            Backbone.history.navigate('about', {'trigger': true});
        },
        goToMission: function(evt){
            Backbone.history.navigate('mission', {'trigger': true});
        },
        goToContact: function(evt) {
            Backbone.history.navigate('contact', {'trigger': true});
        },
        goToIndex: function(evt) {
            Backbone.history.navigate('', {'trigger': true});
        }
    });

    var SearchView = Marionette.ItemView.extend({
        template:templates['templates/search.hbs'],
        tagName: 'div',
        className: 'search-page',
        events: {
            'click .gobutton': 'doSearch'
        },
        doSearch: function() {
            var neighborhood_id = $('#neighborhoods option:selected').val(),
                activity_id = $('#facility__activity option:selected').val(),
                search_url = [
                    'results/',
                    'no_map=true',
                    (neighborhood_id ? '&neighborhoods=' + neighborhood_id.toString() : ''),
                    (activity_id ? '&facility__activity=' + activity_id.toString() : '')
                ].join('');
            Backbone.history.navigate(search_url, {'trigger': true});
        }
    });

    var FooterView = Marionette.ItemView.extend({
        template: templates['templates/footer.hbs'],
        tagName: 'div',
        className: 'footer'
    });

    var AboutView = Marionette.ItemView.extend({
        template: templates['templates/about.hbs'],
        tagName: 'div',
        className: 'about'
    });

    var MissionView = Marionette.ItemView.extend({
        template: templates['templates/mission.hbs'],
        tagName: 'div',
        className: 'mission'
    });
    
    var ContactView = Marionette.ItemView.extend({
        template: templates['templates/contact.hbs'],
        tagName: 'div',
        className: 'contact'
    });

    var ParkView = Marionette.ItemView.extend({
        template: templates['templates/park.hbs'],
        tagName: 'div',
        className: 'detail'
    });

    var ResultItemView = Marionette.ItemView.extend({
        template: templates['templates/resultItem.hbs'],
        className: 'result'
    });

    var ResultsView = Marionette.CompositeView.extend({
        template: templates['templates/results.hbs'],
        itemView: ResultItemView,
        tagname: 'div',
        className: 'results'
    });

    var CarouselPhotoView = Marionette.ItemView.extend({
        template: templates['templates/carouselPhoto.hbs']
    });

    var CarouselView = Marionette.CompositeView.extend({
        template: templates['templates/carousel.hbs'],
        itemView: CarouselPhotoView,
        tagname: 'div',
        className: 'carousel'
    });

    app.Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'about': 'about',
            'mission': 'mission',
            'contact': 'contact',
            'results/:queryString': 'results',
            'parks/:park_slug/': 'park'
        },
        home: function() {
            var searchModel = new SearchModel();
            var searchView = 
            searchModel.once('sync', function() {
              app.getRegion('mainRegion').show(new SearchView({'model': searchModel}));
              $('#loading').css("display", "none"); 
              $('#featured').owlCarousel({
                  navigation: true,
                  items : 3,
                  itemsDesktop : [1199,3],
                  itemsDesktopSmall : [979,3],
                  stopOnHover: true
               });

               $('.carousel').carousel({
                   interval: 3000
               });
            });
            searchModel.fetch();

        },
        about: function() {
          $('#loading').css("display", "none"); 
            app.getRegion('mainRegion').show(new AboutView());
            
        },
        mission: function () {
            app.getRegion('mainRegion').show(new MissionView());
            $('#loading').css("display", "none"); 
        },
        contact: function () {
            app.getRegion('mainRegion').show(new ContactView());
            $('#loading').css("display", "none");
        },
        results: function(queryString) {
            
            var results = new ParksCollection({'queryString': queryString});
            results.fetch({'success': function() {
                app.getRegion('mainRegion').show(new ResultsView({'collection': results}));
                $('#loading').css("display", "none");
                var container = document.querySelector('.results');
                var msnry = new Masonry(container, {
                  gutter: 10, 
                  "isFitWidth": true,
                  transitionDuration: '0s',
                  itemSelector: '.result'
                });
            }});
        },
        park: function (park_slug) {
            var park = new Park({'park_slug': park_slug});
            park.fetch({'success': function() {
                $('#loading').css("display", "none"); 
                var showParkView = app.getRegion('mainRegion').show(new ParkView({'model': park }));

                $('.carousel').carousel({
                   interval: 3000
                });

                $('#orbs').owlCarousel({
                  autoPlay: 3000, //Set AutoPlay to 3 seconds
                  items : 4,
                  navigation: true,
                  itemsDesktop : [1199,3],
                  itemsDesktopSmall : [979,3],
                  stopOnHover: true
                });

                $('#nearby').owlCarousel({
                  autoPlay: 3000, //Set AutoPlay to 3 seconds
                  items : 3,
                  navigation: true,
                  itemsDesktop : [1199,3],
                  itemsDesktopSmall : [979,3],
                  stopOnHover: true
                });

                $('#recommended').owlCarousel({
                  autoPlay: 3000, //Set AutoPlay to 3 seconds
                  items : 3,
                  navigation: true,
                  itemsDesktop : [1199,3],
                  itemsDesktopSmall : [979,3],
                  stopOnHover: true
                });

                $('[data-toggle="tooltip"]').tooltip()

            }});
        }
    });

    app.addInitializer(function(options) {
        app.getRegion('navRegion').show(new HeaderView());
        app.getRegion('footerRegion').show(new FooterView());

        router = new app.Router();
        router.on('route', function() { $('#loading').css("display", "block").on('click', function() { $(this).css('display', 'none') }); })
        app.execute('setRouter', router);
        Backbone.history.start();
        // Backbone.history.navigate('', {'trigger': true});
    });

    return {
        startModule: function(done) {
            app.start({});
        }
    };
});


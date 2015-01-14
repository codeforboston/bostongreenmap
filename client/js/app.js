define([
    'backbone',
    'marionette',
    'paginator',
    'build/templates',
    'masonry',
    'bootstrap',
    'owl',
    'leaflet',
    'tileLayer',
    'chosen'
], function(
    Backbone,
    Marionette,
    paginator,
    templates,
    Masonry,
    owl,
    Leaflet,
    TileLayer
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
            return window.location.origin + '/parks/search/?no_map=true&slug=' + this.park_slug;
        },
        parse: function (response) {
          var attributes = {};
          _.each(response.parks, function(attribute, key) {
            _.each(attribute, function(attribute, key) {
              attributes[key] = attribute;
            })
          });
          return attributes;
        }
    });
    
    var SearchModel = Backbone.Model.extend({
        url: function() {
            return window.location.origin + '/parks/get_neighborhoods_and_activities_list/';
        },
        parse: function(response) {
            var data = {'neighborhoods': [], 'activities': [], 'featured_parks': [], 'hero_images': []};
            _.each(response.neighborhoods, function(neighborhood) {
                data.neighborhoods.push({'id': neighborhood.id, 'name': neighborhood.name});
            });
            _.each(response.activities, function(activity) {
                data.activities.push({'id': activity.id, 'name': activity.name});
            });
            _.each(response.featured_parks, function(featured_park) {
                data.featured_parks.push({'id': featured_park.id, 'name': featured_park.name, 'url': featured_park.url, 'images': featured_park.images });
            });
            _.each(response.hero_images, function(hero_image) {
                data.hero_images.push({'src': hero_image.src, 'large_src': hero_image.large_src });
            });
            return data;
        } 
    });

    var ParksCollection = Backbone.PageableCollection.extend({
        model: Park,
        initialize: function(params) {
            this.queryString = params.queryString
        },
        url: function() {
            var search_url = 'parks/search/?' + this.queryString;
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
        },
        queryParams: {
          pageSize: null,
          totalPages: "pages"
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
        },
        onShow: function() {
          $(".parkfilter").chosen()
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
        events: {
          'click #toggle': 'toggleContent'
        },
        initialize: function() {
          if (this.showMapState === undefined) {
            this.showMapState = false;
          }
          return this;
        },
        toggleContent: function (evnt) {
          if (this.showMapState === false) {
            this.showMap();
          } else {
            this.hideMap();
          }
        },
        showMap: function () {
          this.$el.find('#map').show();
          this.$el.find('#carousel-images-container').hide();
          this.showMapState = true;

          app.map.invalidateSize();

          // the way GEOS returns #coords, we have to reorder the lat/lngs. 
          app.map.fitBounds([
                  [this.model.attributes.bbox[0][1], this.model.attributes.bbox[0][0]],
                            [this.model.attributes.bbox[1][1], this.model.attributes.bbox[1][0]]
                          ]);

        },
        hideMap: function () {
          this.$el.find('#map').hide();
          this.$el.find('#carousel-images-container').show();
          this.showMapState = false;
        },
        template: templates['templates/park.hbs'],
        tagName: 'div',
        className: 'detail',
        onShow: function() {
          
            var self = this;
            self.$('#carousel-images-container').owlCarousel({
                autoPlay: true, //Set AutoPlay to 3 seconds
               items: 1,
               stopOnHover: true,
               singleItem: true
            });

            self.$('#orbs').owlCarousel({
              autoPlay: 3000, //Set AutoPlay to 3 seconds
              items : 4,
              navigation: true,
              itemsDesktop : [1199,3],
              itemsDesktopSmall : [979,3],
              stopOnHover: true
            });

            self.$('#nearby').owlCarousel({
              autoPlay: 3000, //Set AutoPlay to 3 seconds
              items : 3,
              navigation: true,
              itemsDesktop : [1199,3],
              itemsDesktopSmall : [979,3],
              stopOnHover: true
            });

            self.$('#recommended').owlCarousel({
              autoPlay: 3000, //Set AutoPlay to 3 seconds
              items : 3,
              navigation: true,
              itemsDesktop : [1199,3],
              itemsDesktopSmall : [979,3],
              stopOnHover: true
            });

            self.$('[data-toggle="tooltip"]').tooltip()

            app.map = L.map('map', {scrollWheelZoom: false});

            L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
                subdomains: 'abcd',
                minZoom: 0,
                maxZoom: 18
            }).addTo(app.map);

            var style = {
                clickable: true,
                color: "#00c800",
                weight: 0,
                opacity: 1,
                fillColor: "#00DC00",
                fillOpacity: 0.6
              };
            var hoverStyle = {
                "fillOpacity": 0.9
            };
            var geojsonURL = 'http://104.131.99.131:8080/osm-processed_p1/{z}/{x}/{y}.json';
            var geojsonTileLayer = new L.TileLayer.GeoJSON(geojsonURL, {
                    clipTiles: true,
                    unique: function (feature) { 
                        return feature.id;
                    }
                }, {
                    style: function(feature, layer) {
                        return style;
                    },
                    reuseTiles: true,
                    onEachFeature: function (feature, layer) {
                        if (feature.properties) {
                            var popupString = '<div class="popup">';
                            for (var k in feature.properties) {
                                var v = feature.properties[k];
                                popupString += k + ': ' + v + '<br />';
                            }
                            popupString += '</div>';
                            layer.bindPopup(popupString);
                        }
                        if (!(layer instanceof L.Point)) {
                            layer.on('mouseover', function () {
                                layer.setStyle(hoverStyle);
                            });
                            layer.on('mouseout', function () {
                                layer.setStyle(style);
                            });
                        }
                    }
                }
            );
 
            app.map.addLayer(geojsonTileLayer);

            //FIXME: I don't know the best design approach to lazy-loading relational 1:m models
            var url = window.location.origin + '/parks/' + self.model.attributes.id + '/facilities/';

            $.get(url, function(response) {
              var myStyle = {
                  "color": "#ff7800",
                  "weight": 5,
                  "opacity": 0.65
              };

              L.geoJson(response, {
                  style: myStyle,
                  pointToLayer: function(feature, latlng) {
                    return new L.CircleMarker(latlng, {radius: 10, fillOpacity: 0.85});
                  }
              }).addTo(app.map);
            });
        }
    });

    var ResultItemView = Marionette.ItemView.extend({
        template: templates['templates/resultItem.hbs'],
        className: 'result'
    }); 

    var ResultsView = Marionette.CompositeView.extend({
        events: {
          'click #previous-button': 'getLastPage',
          'click #next': 'getNextPage'
        },
        collection: ParksCollection,
        initialized: false,
        getNextPage: function(evnt) {
          var that = this;
          this.collection.getNextPage({remove:false, success: function() { }});
          this.initialized = true;
          
        },
        getLastPage: function(evnt) {
          this.collection.getLastPage();
        },
        template: templates['templates/results.hbs'],
        childView: ResultItemView,
        tagname: 'div',
        className: 'results',        
        onShow: function () {
          var self = this;

          $('#loading').css("display", "none");

          self.msnry = new Masonry(self.el, {
            // transform: 'scale(15)',
            // gutter: 10,
            // columnWidth: 300,
            // "isFitWidth": true,
            // transitionDuration: '0s',
            itemSelector: '.result'
          }); 
        }, 
        collectionEvents: {
          "add": "modelAdded"
        },
        modelAdded: function(model) {
          console.log(model);
        },
        onRenderCollection: function(collection) {
          console.log(collection);
        },
        onAddChild: function (childView) {
          if(this.initialized) {
            this.msnry.appended(childView.el);  
          }
        }
    });

    var ResultsLayout = Backbone.Marionette.LayoutView.extend({
      onShow: function() {
        this.getRegion('results').show(new ResultsView({'collection': this.collection}))
      },
      events: {
        "click #next": "getNext"
      },
      getNext: function () {
        var that = this;
        this.results.currentView.collection.getNextPage({remove:false, success: function() { }});
        this.results.currentView.initialized = true;

      },
      className: "resultsSection",
      collection: ParksCollection,
      template: templates['templates/all_results.hbs'],
      regions: {
        results: "#results",
        next: "#next"
      }
    });

    app.Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'about': 'about',
            'mission': 'mission',
            'contact': 'contact',
            'results/:queryString': 'results',
            'parks/:park_slug/': 'park',
            'parks/:park_slug/:map': 'park'

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

               $('#carousel-images-container').owlCarousel({
                  autoPlay : true, // Show next and prev buttons
                  slideSpeed : 300,
                  paginationSpeed : 400,
                  singleItem: true
                  // items : 2 //10 items above 1000px browser width
                  // itemsDesktop : [1000,1] //5 items between 1000px and 901px
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
              app.getRegion('mainRegion').show(new ResultsLayout({'collection': results}));
            }});
        },
        park: function (park_slug, map) {
            var park = new Park({'park_slug': park_slug});
            park.fetch({'success': function() {
                if(map) {
                  map = true;
                } else {
                  map = false;
                }

                $('#loading').css("display", "none");
                var parkView = new ParkView({'model': park, 'showMapState': map });
                parkView.showMapState=map;
                app.getRegion('mainRegion').show(parkView);
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
    });

    return {
        startModule: function(done) {
            app.start({});
        }
    };
});


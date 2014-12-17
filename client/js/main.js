requirejs.config({
    shim: {
        underscore: {
            exports: '_'
        },
        jquery: {
            exports: '$'
        },
        backbone: {
            exports: 'Backbone',
            deps: ['underscore', 'jquery']
        },
        handlebars: {
            exports: 'Handlebars'
        },
        marionette: {
            deps: ['underscore', 'jquery', 'backbone'],
            exports: 'Marionette'
        },
        page: {
            exports: 'page'
        },
        bootstrap: {
            deps: ['jquery']
        },
        owl: {
            deps: ['jquery']
        },
        masonry: {
            exports: 'Masonry'
        },
        leaflet: {
            exports: 'Leaflet'
        },
        topojson: {
            exports: 'topojson'
        }
    },
    baseUrl: '/static',
    paths: {
        underscore: 'lib/underscore-1.5.2.min',
        jquery: 'lib/jquery-1.10.2.min',
        backbone: 'lib/backbone-1.1.0.min',
        marionette: 'lib/backbone.marionette-1.5.1.min',
        handlebars: 'lib/handlebars-runtime.1.3.0.min',
        js: 'js',
        build: 'build',
        bootstrap: 'lib/bootstrap.min',
        owl: 'lib/owl.carousel.min',
        masonry: 'lib/masonry.pkgd.min',
        leaflet: 'lib/leaflet',
        topojson: 'lib/topojson'
    }
});

require(['js/app', 'js/helpers'], function(app, helpers) {
    helpers.register();
    app.startModule();
});

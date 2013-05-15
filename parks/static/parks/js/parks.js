window.bgm = window.bgm || {};

(function(){

  var defaultZoom = 13,
      searchUrl = '/parks/search/',
      parks, // park properties
      parkGeoms, // park geometries
      parkDetailTemplateSource = $("#detail-template").html(), // templates
      parkDetailTemplate = Handlebars.compile(parkDetailTemplateSource),
      parkPopupTemplateSource = $("#parkPopup-template").html(),
      parkPopupTemplate = Handlebars.compile(parkPopupTemplateSource),
      facilityPopupTemplateSource = $("#facilityPopup-template").html(),
      facilityPopupTemplate = Handlebars.compile(facilityPopupTemplateSource),
      activitiesTemplateSource = $("#activities-template").html(),
      activitiesTemplate = Handlebars.compile( activitiesTemplateSource );


  //-- Urls and hashes --//

  window.onpopstate = function(event) {
    if ( 'state' in window.history && event.state !== null) {
      // back button for exploring filters
      // FIXME: back to park detail doesn't work
      set_dropdowns( event.state );
      filter_parks( searchUrl + "?" + $.param( event.state ) ); 
    } else {
      
      var params = $.url().attr('query'),
          hash = window.location.hash,
          url = searchUrl;

      if ( params !== "" ) {
        set_dropdowns( $.url().param() );
        load_parkGeoms( searchUrl + '?' + params );
      } else if ( hash ) {
        var slug = hash.split("/")[2];
        load_parkGeoms( searchUrl + '?slug=' + slug );
      } else {
        load_parkGeoms( url, defaultZoom );
      }
    }
  };


  //-- Layout adjustments --//

  // resize map_canvas
  var topmargin = $(".navbar").height();
  $("#map_canvas").css("height", ($(window).height() - topmargin));
  $(window).on("resize", function(e){
    $("#map_canvas").css("height", ($(window).height() - topmargin));
  });

  // comboboxes instead of dropdowns
  $(".chzn-select").chosen();

  // adjust map width based on slider
  $("#slider")
    .on( "shown", function () {
      $("#map_canvas").width( $(window).width() - $("#slider").width() );
      map.invalidateSize( false );
    })
    .on( "hidden", function() {
      $("#map_canvas").width( $(window).width() );
      map.invalidateSize( false );
    });


  //-- Navbar dropdowns --//

  // get or set parkfilter dropdown values
  function set_dropdowns( config ) {
    // set dropdown values
    for ( var k in config ) {
      $( "#" + k ).val( config[k] ).trigger( "liszt:updated" );
    }
  }
  function get_dropdowns() {
    var params = {};
    $(".parkfilter").each( function( index ) {
      if ( $(this).val() ) params[ $(this).attr("id") ] = $(this).val();
    });
    return params;
  }

  // load new parks on dropdown change
  $("#neighborhoods, #facility__activity").on("change", function() {
    var params = get_dropdowns();
    filter_parks( searchUrl + "?" + $.param(params) );
    history.pushState(params, "BostonGreenMap - Find Your Space!", "?" + $.param(params));
  });


  //-- Map setup --//

  // initialize map
  var basemap = new L.MAPCTileLayer("basemap"),
      trailmap = new L.MAPCTileLayer("trailmap"),
      bing = new L.BingLayer("An8pfp-PjegjSInpD2JyXw5gMufAZBvZ_q3cbJb-kWiZ1H55gpJbxndbFHPsO_HN", "Aerial"),
      boston = new L.LatLng(42.357778, -71.061667),
      map = new L.Map( "map_canvas", {
        minZoom: 9,
        maxZoom: 17,
        zoom: defaultZoom,
        center: boston,
        layers: [basemap]
      });

  // initialize Parklayer
  var parkLayer = L.geoJson(null, {
    style: {
      color: "#00c800",
      weight: 1.2,
      opacity: 1,
      fillColor: "#00DC00",
      fillOpacity: 0.6
    },
    onEachFeature: function (feature, layer) {

      var park = $.extend( parks[feature.id], { id: feature.id });
      var html = parkPopupTemplate(park);
      var div = L.DomUtil.create( "div" );

      $(div)
        .addClass( "popup" )
        .append( html );

      $(div).find(".info").first().on("click", function( event ) {
        event.preventDefault();
        show_parkDetail( park );
      });
      $(div).find(".zoom").first().on("click", function( event ) {
        event.preventDefault();
        var park = $.extend( parks[feature.id], { id: feature.id });
        zoomto_park( park );
      });

      layer.bindPopup( div );
    },
    filter: function (feature, layer) {
      return true;
    }
  }).addTo( map );
  // initialize Facilitylayer
  var facilityLayer = L.geoJson(null).addTo( map );

  // initialize Controls
  map.addControl(new L.Control.Layers( {
      "MAPC Basemap": basemap, 
      "MAPC Trailmap": trailmap,
      "Bing Aerial": bing 
    }, {
      "Park Facilities": facilityLayer,
      "Parks": parkLayer
    } )
  );
  // Geolocation control
  var locateMeControl = new L.control({
    position: "topleft"
  });
  locateMeControl.onAdd = function (map) {
    // Leaflet control container DOM element
    var div = L.DomUtil.create('div', 'leaflet-control-zoom leaflet-bar leaflet-control');
    var $link = $( "<a/>", {
      class: "leaflet-control-geoloc",
      title: "Locate Me"
    }).appendTo( $(div) );
    $link.on( "click", function( event ) {
      event.preventDefault();
      // geolocate
      map.locate({setView: true, maxZoom: 17});
    });
    return div;
  }; 
  map.addControl(locateMeControl);


  //-- Retrieve Park Data --//

  // loads all park geometries
  function load_parkGeoms( url, zoom ) {
    $.getJSON("/static/parks/data/parks.topo.json", function (data) {
      var parksGeojson = topojson.object(data, data.objects.parks);
      parkGeoms = parksGeojson.geometries;
      filter_parks( url, zoom );
    });
  }

  // load park facilities
  function load_parkFacilities( parkId ) {
    var url = "/parks/" + parkId + "/facilities/",
        activities = [];

    $.getJSON(url, function (data) {

      facilityLayer.options = {
        pointToLayer: function( feature, latlng ) {
          var icon = new L.Icon({
            iconUrl: feature.properties.icon,
            shadowUrl: null,
            iconSize: new L.Point(32, 37),
            shadowSize: null,
            iconAnchor: new L.Point(16, 37),
            popupAnchor: new L.Point(2, -32)
          });
          return new L.Marker( latlng, {
              icon: icon
          })
        },
        onEachFeature: function ( feature, layer ) {
          $.merge(activities, feature.properties.activities);

          var html = facilityPopupTemplate( feature.properties );
          var div = L.DomUtil.create( "div" );

          $(div)
            .addClass( "popup" )
            .append( html );

          layer.bindPopup( div );
        }
      }

      facilityLayer.addData( data );

      // render activity list
      var uniqueActivities = [];
      $.each(activities, function(i, activity){
        if($.inArray( activity, uniqueActivities) === -1 ) uniqueActivities.push( activity );
      });

      // update activity listing
      var html = activitiesTemplate( { activities: uniqueActivities.sort() } );
      $("#content .park-detail #activities").append( html );

    });
  }


  //-- Present Data in UI --//

  // map search result and update typeahead with filtered parks
  function filter_parks( url, zoom ) {
    $.getJSON( url , function(data) {

      var parkNames = [],   // park name list for typeahead
          parkFilter = [],  // park id list for map
          parkIds = {};     // park name->id mapping for typeahead
                            // parkDetail lookup
      parks = data;

      for(var id in parks) { // iterate of park ids
        parkNames.push( parks[id].name );
        parkFilter.push( parseInt(id) );
        parkIds[ parks[id].name ] = id;
      }

      // update typeahead
      var autocomplete = $('#parkname').typeahead({
        updater: function (item) {
          // var parkUrl = parks[ item ].url;
          // window.location.assign( window.location.origin + parkUrl );
          var parkId = parseInt( parkIds[ item ] );
          var park = $.extend( parks[ parkId ], { id: parkId });
          show_parkDetail( park );
          zoomto_park( park );
          return item;
        }
      });
      autocomplete.data('typeahead').source = parkNames;
      
      // remove existing parks from map
      parkLayer.clearLayers();

      // re-define GeoJSON filter
      parkLayer.options.filter = function(feature, layer) {
        if ( $.inArray( feature.id, parkFilter ) == -1 ) return false;
        return true;
      };

      // add parkgeometries to layer
      if ( parkFilter.length > 0 ) {
        var len = parkGeoms.length;
        while (len--) {
          parkLayer.addData(parkGeoms[len]);        
        }
        // zoom to park bounds or default zoomlevel
        if (zoom === undefined) {
          map.fitBounds(parkLayer.getBounds());
        } else {
          map.setZoom( zoom );
        }
      }

      // single park view
      if ( parkNames.length === 1 ) {
        show_parkDetail( parks[id] );
      }

    });
  };

  // park detail slider
  function show_parkDetail( park ) {
    // content
    var html = parkDetailTemplate(park);
    $("#content").html( html );

    // image slideshow
    if ( park.images.length > 1 ) {
      $("#parkimages").slidesjs({
        width: 250,
        height: 250,
        navigation: false,
        pagination: false
      });
      $(".slidesjs-navigation").show()
    } else {
      $(".slidesjs-navigation").hide()
    }

    // load park facilities
    load_parkFacilities( park.id );

    // show details
    $("#slider").collapse("show");

    // push url
    // FIXME: replace root
    history.pushState(park, park.name + " | Boston Green Map", "#" + park.url );
  }


  //-- Utilities --//

  // return LatLngBounds based on parkid
  function get_parkBounds( parkid ) {
    var len = parkGeoms.length;
    while (len--) {
      if ( parkGeoms[len].id == parkid ) {     
        var parkGeom = new L.GeoJSON( parkGeoms[len] );
        return parkGeom.getBounds();
      }     
    }
    return false;
  }

  // zoom to park
  function zoomto_park( park ) {
    // zoom map to park
    var parkBounds = get_parkBounds( park.id );
    map.fitBounds( parkBounds );
  }

})();

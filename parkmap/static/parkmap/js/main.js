$(function() {
    
    // initialize map
    var mapclayer = "basemap"
    var parkmap = new google.maps.Map(document.getElementById("map_canvas"), {
        zoom: 13,
        center: new google.maps.LatLng(42.31, -71.032),
        minZoom: 10,
        maxZoom: 17,
        mapTypeControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
            mapTypeIds: [mapclayer, google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.SATELLITE], //,
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        panControl: false,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL
        },
        streetViewControl: false
    });

    parkmap.mapTypes.set(mapclayer, new google.maps.MAPCMapType(mapclayer));
    parkmap.setMapTypeId(mapclayer);

    // encoded polylines for google maps
    var decodeLevels = function(encodedLevelsString) {
        var decodedLevels = [];
        for (var i = 0; i < encodedLevelsString.length; ++i) {
            var level = encodedLevelsString.charCodeAt(i) - 63;
            decodedLevels.push(level);
        }
        return decodedLevels;
    }

    // load large parks
    var loadparks = function(options) {
        // FIXME: add bbox parameter to park query
        var param = options || parkfilter || {}; 
        param["format"] = "json";

        $.getJSON('/api/v1/park/', 
            param,
            function(data) {
                var parks = data.objects;
                var latlngbounds = new google.maps.LatLngBounds();
                $.each(parks, function(key, park) {
                    var parkPoly = new google.maps.Polygon({
                        paths: google.maps.geometry.encoding.decodePath(park.geometry.points),
                        levels: decodeLevels(park.geometry.levels),
                        fillColor: '#00DC00',
                        fillOpacity: 0.8,
                        strokeWeight: 0,
                        zoomFactor: park.geometry.zoomFactor, 
                        numLevels: park.geometry.numLevels,
                        map: parkmap
                    });
                    if (param["zoomtoextent"] === true) {
                        var latlngs = parkPoly.getPath().getArray();
                        for ( var j = 0; j < latlngs.length; j++ ) {
                            latlngbounds.extend(latlngs[j]);
                        }
                    }
                });
                if (param["zoomtoextent"] === true) {
                    // zoom map to parks extent and adjust zoom
                    parkmap.fitBounds(latlngbounds);
                }
        });
    };
    loadparks();
});


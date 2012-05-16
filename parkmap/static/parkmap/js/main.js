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

    // load parks
    var loadparks = function(filteroptions, mapoptions) {
        
        // prioritizes parkfilter defined on a template page over options argument and finally defaults to empty object
        var filterparam = (typeof parkfilter === 'undefined') ? ((typeof filteroptions === 'undefined') ? {} : filteroptions) : parkfilter;
        filterparam["format"] = "json";
        // same spiel for map configuration, used to specify extent and additional layers
        var mapparam = (typeof mapconf === 'undefined') ? ((typeof mapoptions === 'undefined') ? {} : mapoptions) : mapconf;
        
        // TODO: add bbox parameter to park query
        $.getJSON('/api/v1/park/', 
            filterparam,
            function(data) {
                var parks = data.objects;
                var latlngbounds = new google.maps.LatLngBounds();
                $.each(parks, function(key, park) {
                    var parkPoly = new google.maps.Polygon({
                        paths: google.maps.geometry.encoding.decodePath(park.geometry.points),
                        levels: decodeLevels(park.geometry.levels),
                        fillColor: '#00DC00',
                        fillOpacity: 0.6,
                        strokeWeight: 0,
                        zoomFactor: park.geometry.zoomFactor, 
                        numLevels: park.geometry.numLevels,
                        map: parkmap
                    });
                    if (mapparam["zoomtoextent"] === true) {
                        var latlngs = parkPoly.getPath().getArray();
                        for ( var j = 0; j < latlngs.length; j++ ) {
                            latlngbounds.extend(latlngs[j]);
                        }
                    }
                });
                if (mapparam["zoomtoextent"] === true) {
                    // zoom map to parks extent and adjust zoom
                    parkmap.fitBounds(latlngbounds);
                }
                if (mapparam["loadfacilities"]) loadfacilities(mapparam["loadfacilities"]);
        });
    };
    loadparks();

    // load facitlies
    var loadfacilities = function(options) {
        var param = options;
        param["format"] = "json";
        $.getJSON('/api/v1/facility/',
            param,
            function(data) {
                var facilities = data.objects; 
                $.each(facilities, function(key, facility) {
                    var facilityicon = facility["icon"];
                    var facilitylatlng = new google.maps.LatLng(facility["geometry"]["coordinates"][1], facility["geometry"]["coordinates"][0]);
                    var facilitymarker = new google.maps.Marker({
                        position: facilitylatlng,
                        title: facility["name"],
                        map: parkmap,
                        icon: facilityicon
                    });
                });
        });
    };
});




    // map
    // var parkmap = new google.maps.Map(document.getElementById("map_canvas"));
    var parkmap = new google.maps.Map(document.getElementById("map_canvas"), {
        zoom: 13,
        minZoom: 10,
        maxZoom: 16,
        center: new google.maps.LatLng(42.33, -71.061667), //42.357778
        mapTypeControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
            mapTypeIds: ["simple",google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.SATELLITE],
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        panControl: false,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL
        },
        streetViewControl: false
    });

    // simple map style
    var simple_style =  [
        {
            featureType: "administrative",
            elementType: "geometry",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "administrative",
            elementType: "labels",
            stylers: [
                { visibility: "off" },
                { hue: "#d70000" },
                { lightness: 10 },
                { saturation: -95 }
            ]
        },{
            featureType: "landscape",
            elementType: "all",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "poi",
            elementType: "geometry",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "poi",
            elementType: "labels",
            stylers: [
                { visibility: "off" },
            ]
        },{
            featureType: "transit",
            elementType: "all",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "transit.line",
            elementType: "geometry",
            stylers: [
                { hue: "#ff0000" },
                { visibility: "on" },
                { lightness: -20 }
            ]
        },{
            featureType: "road",
            elementType: "geometry",
            stylers: [
                { hue: "#d70000" },
                { visibility: "simplified" },
                { lightness: 10 },
                { saturation: -95 }
            ]
        },{
            featureType: "road",
            elementType: "labels",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "water",
            elementType: "geometry",
            stylers: [
                { visibility: "on" },
                { hue: "#0091ff" },
                { lightness: 30 },
                { saturation: -100 }
            ]
        },{
            featureType: "water",
            elementType: "labels",
            stylers: [
                { visibility: "off" }
            ]
        }
    ];

    var simple_options = {
        name: "Gray Map"
    }

    var simple = new google.maps.StyledMapType(simple_style, simple_options);

    parkmap.mapTypes.set("simple", simple);
    parkmap.setMapTypeId("simple");

    // encoded polylines for google maps
    var decodeLevels = function(encodedLevelsString) {
        var decodedLevels = [];
        for (var i = 0; i < encodedLevelsString.length; ++i) {
            var level = encodedLevelsString.charCodeAt(i) - 63;
            decodedLevels.push(level);
        }
        return decodedLevels;
    }

var parkp = null;

function filter_parks(slug){
    url = '/api/v1/park/?format=json&slug='+slug;
    $.getJSON(url, function(data) {
        var parks = data.objects;
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
            parkp = parkPoly;
        });
    });
}

$(function() {
    // load parks
    // FIXME: add bbox parameter to park query
    //filter_parks();
    $.getJSON('/api/v1/park/?format=json', function(data) {
        var parks = data.objects;
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
        });
    });
    
});


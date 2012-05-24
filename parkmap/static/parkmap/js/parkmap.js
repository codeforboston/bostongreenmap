// bostonparks object
var bp = {
  
  // custom basemap layer
  mapclayer: "basemap",

  // array with currently visible map features (parks, facilites)
  overlays: [],

  // map configurations
  mapconf: {},

  // paginaton threshold
  listlimit: 10,

  update_second_dropdown: function(search_type, filter_type, filter,value_key,django_neighborhood) {
    /*
    Pass in:
      The type of the second box for search_type
      The type of the first box for filter_type;
      The value to filter on for filter
      The value_key is whether to use 'id' or 'slug'
    */
    //Set the first item in the dropdown box
    var out = '<option value="">Select Your ';
    switch(search_type) {
    case 'neighborhood':
      out += 'Neighborhood/Town';
      break;
    case 'parktype':
      out += "Park Type";
      break;
    case 'activity':
      out += "Activity";
      break;
    }
    out += "</option>";
    $.ajax({
      url:'/api/v1/'+search_type+'/?format=json&limit=1000&'+filter_type+'='+filter,
      dataType:'json',
      success:function(json){
        $.each(json['objects'], function(key, obj) {
          //check whether the value returned is supposed to be an id or a slug.
          //Create the new item in the dropdown list.
          if ( obj['slug'] == django_neighborhood){
            out+= '<option selected="selected" value="'+escape(obj[value_key])+'">' + obj['name']+'</option>';
            //coming in from neighborhood page
          } else {
            out+= '<option value="'+escape(obj[value_key])+'">' + obj['name']+'</option>';
          }
        });
        //replace the items in the dropdown list, and select the first element
        $("#neighborhood_"+search_type).html(out);
        $("#neighborhood_"+search_type).val($("#neighborhood_"+search_type+" option:first").val());
        if (typeof(django_neighborhood) != "undefined"){
          //Select the neighborhood passed in via the page parameter and auto search
          var neigh = $('#neighborhood_neighborhood option[value="'+django_neighborhood+'"]');
          neigh.attr('selected','selected');
          bp.play_get_parks(0);
        }
      }
    });
  },

  update_parklist: function(url, parkfilter){
      
    // don't use parkfilter if we have url
    if (url) {
      parkfilter = null;
    } else {
      url = "/api/v1/park/";
      // parkfilter defaults  
      parkfilter["format"] = "json";
      parkfilter["limit"] = this.listlimit;
    }

    $.getJSON(url,
      parkfilter,
      function(data) {
        var out = "";
        var latlngs = [];
        bp.clearmap();
        $.each(data['objects'], function(key, park) {
          var p = "<h3><a href='/park/"+park['slug']+"'>"+park['name'] + "</a></h3>";

          if (park['description']) {p += "<p>"+ bp.truncate(park['description']) +"</p>";};
          // add park to map
          parkLatlngs = bp.renderpark(park["geometry"], {
            "name": park["name"],
            "description": park["description"]
          });
          latlngs.push.apply(latlngs, parkLatlngs);
          // adjust map extent
          if (bp.mapconf["zoomtoparks"]) bp.zoomtoparks(latlngs);
          
          out += p;
        });

        // show facilities
        if (bp.mapconf["showfacilites"] ) bp.loadfacilities({
          "park__neighborhoods": parkfilter["neighborhood"],
          "activity": parkfilter["activity"]
        });
        
        var previous = false;
        // FIXME: we need some of the parkfilter options (activity and neighborhood) for facility queries
        if(data['meta']['previous']){
            out += '<a href="javascript:void(0)" onclick="bp.update_parklist(\''+data['meta']['previous']+'\')">PREVIOUS</a>';
            previous = true;
          }
        if(data['meta']['next']){
            if(previous){ out += "&nbsp;&nbsp;";}
            out += '<a href="javascript:void(0)" onclick="bp.update_parklist(\''+data['meta']['next']+'\')">NEXT</a>';
          }
        $("#parklist").html(out);
    });
  },

  play_get_parks: function(offset) {
    var neighborhood = $("#neighborhood_neighborhood").val();
    var activity = $("#neighborhood_activity").val();
    if (activity === ""){ return;}
    if (neighborhood=== ""){ return;}
    var activities = new Array();
    $("#parklist").html("");
    this.update_parklist(null, {
      offset: offset,
      neighborhood: neighborhood,
      activity: activity
    });
  },

  explore_filter_activities: function(neighborhood_slug,parktype_id){
    var out = "";
     $.ajax({
       //probe the correct park url
       url:'/api/v1/exploreactivity/?format=json&limit=1000&neighborhood='+neighborhood_slug+'&parktype='+parktype_id,
       //url:url,
       dataType:'json',
       success:function(json){
         $.each(json['objects'], function(key, obj) {
           //check whether the value returned is supposed to be an id or a slug.
           //Create the new item in the dropdown list.
           out+= '<input type="checkbox" class="activity_checkbox" name="activity_checkboxes" value="'+obj['id']+'">'+obj['name']+'<br>';
         });
         //replace the items in the dropdown list, and select the first element
         $("#activity_checkboxes").html(out);
       }
     });
  },

  explore_filter_parkactivities: function(){
    var neighborhood = $("#neighborhood_neighborhood").val();
    var parktype = $("#neighborhood_parktype").val();
    var activities = new Array();
    $('#activity_checkboxes input:checked').each(function() {
      activities.push($(this).val());
    });
    $("#parklist").html("");
    $("#facilitylist").html("");
    if (activities.length == 0){
      return;
    }

    // find parks
    // find facilities

    activities = activities.join(",");
    var latlngs = [];
    bp.clearmap();
    $.ajax({
       //probe the correct park url
       url:'/api/v1/explorepark/?format=json&limit=1000&neighborhood='+neighborhood+'&parktype='+parktype+'&activity_ids='+activities,
       //url:url,
       dataType:'json',
       success:function(json){
         var out = "";
          $.each(json['objects'], function(key, park) {
             //DO SOMETHING BETTER HERE USING THE DATA.
          // out+= obj['name'] + " - " + obj['os_id']+'<br>';

          var p = "<h3><a href='/park/"+park['slug']+"'>"+park['name'] + "</a></h3>";
          if (park['description']) {p += "<p>"+ park['description']+"</p>";};
          out += p;

          // add park to map
          parkLatlngs = bp.renderpark(park["geometry"], {
            "name": park["name"],
            "description": park["description"]
          });
          latlngs.push.apply(latlngs, parkLatlngs);
          // adjust map extent
          if (bp.mapconf["zoomtoparks"]) bp.zoomtoparks(latlngs);


         });
         $("#parklist").html(out);
       }
     });


    $.ajax({
     url:'/api/v1/explorefacility/?format=json&limit=1000&neighborhood='+neighborhood+'&parktype='+parktype+'&activity_ids='+activities,
     dataType:'json',
     success:function(json){
      var out = "";
       $.each(json['objects'], function(key, facility) {
          //DO SOMETHING BETTER HERE USING THE DATA.
          // out += obj['name'] + " - " + obj['id']+'<br>';
          // add facility to map
          bp.renderfacility(facility["geometry"], {
            icon: facility["icon"],
            name: facility["name"],
            activity_string: facility["activity_string"],
            admin_url: facility["admin_url"]
          })

       });
       // FIXME: list should be nested with parks, not attached
       // $("#facilitylist").html(out);
     }
   });
  },

  // load parks and render on map
  loadparks: function(parkfilter, mapconf) {
      
    parkfilter["format"] = "json";
    bp.clearmap();
    var latlngs = [];
    // TODO: add bbox parameter to park query
    $.getJSON('/api/v1/park/', 
      parkfilter,
      function(data) {
        var parks = data.objects;
        
        $.each(parks, function(key, park) {

          parkLatlngs = bp.renderpark(park["geometry"], {
            "name": park["name"],
            "description": park["description"]
          });
          latlngs.push.apply(latlngs, parkLatlngs);
          // adjust map extent
          if (bp.mapconf["zoomtoparks"]) bp.zoomtoparks(latlngs);

          // show facilities
          // FIXME: track parks in array and filter with '__in' parameter in one request
          if (bp.mapconf["showfacilites"] ) bp.loadfacilities({
            "park": park["os_id"]
          });

        });
    });
  },

  // loac facilities and render on map
  loadfacilities: function(facilityfilter) {

    facilityfilter["format"] = "json";

    $.getJSON('/api/v1/facility/',
      facilityfilter,
      function(data) {
        var facilities = data.objects; 
        $.each(facilities, function(key, facility) {

          // add facilities to map
          bp.renderfacility(facility["geometry"], {
            icon: facility["icon"],
            name: facility["name"],
            activity_string: facility["activity_string"],
            admin_url: facility["admin_url"]
          })

      });
    });
  },

  renderpark: function(geometry, properties) {
    // accepts multipart geometries and property object
    var latlngs = [];
    $.each(geometry, function(key, part) {
        var parkPoly = new google.maps.Polygon({
          paths: google.maps.geometry.encoding.decodePath(part["points"]),
          levels: bp.decodeLevels(part["levels"]),
          fillColor: '#00DC00',
          fillOpacity: 0.6,
          strokeWeight: 0,
          zoomFactor: part["zoomFactor"], 
          numLevels: part["numLevels"],
          map: bp.map
        });
        // extend latlngs
        latlngs.push.apply(latlngs, parkPoly.getPath().getArray());
        // track overlay
        bp.overlays.push(parkPoly);
    });
    return latlngs;
  },

  renderfacility: function(geometry, properties) {
    // marker with custom icon
    var facilityicon = properties["icon"];
    var facilitylatlng = new google.maps.LatLng(geometry["coordinates"][1], geometry["coordinates"][0]);
    var facilitymarker = new google.maps.Marker({
      position: facilitylatlng,
      title: properties["name"],
      map: bp.map,
      icon: facilityicon
    });
    // track overlay
    bp.overlays.push(facilitymarker);
    // marker infowindow
    var facilityinfocontent = "<strong>" + properties["name"] + "</strong><br> \
                               Activities: " + properties["activity_string"];
    if (typeof staff !== 'undefined' && staff === true) {
      facilityinfocontent += "<br><a href='" + properties["admin_url"] + "'>Edit</a>";
    }
    var facilityinfo = new google.maps.InfoWindow({
      content: facilityinfocontent
    });
    google.maps.event.addListener(facilitymarker, 'click', function() {
      facilityinfo.open(bp.map, facilitymarker);
    });
  },

  zoomtoparks: function(latlngs) {
    // accepts array of lat/long pairs
    var latlngbounds = new google.maps.LatLngBounds();
    for ( var i = 0; i < latlngs.length; i++ ) {
      latlngbounds.extend(latlngs[i]);
    }
    bp.map.fitBounds(latlngbounds);
  },

  // remove all overlays (parks, facilities) from map
  clearmap: function() {
    while(this.overlays[0]){
      this.overlays.pop().setMap(null);
    }
  },

  // encoded polylines for google maps
  decodeLevels: function(encodedLevelsString) {
      var decodedLevels = [];
      for (var i = 0; i < encodedLevelsString.length; ++i) {
          var level = encodedLevelsString.charCodeAt(i) - 63;
          decodedLevels.push(level);
      }
      return decodedLevels;
  },

  truncate: function(string, nrchars) {
    // accepts a string and a number of characters the string shcould be truncated to
    var nrchars = nrchars || 100;
    var string = string.trim().substring(0, nrchars).split(" ").slice(0, -1).join(" ") + "...";
    return string;
  }
}


// add google map
bp.map = new google.maps.Map(document.getElementById("map_canvas"), {
  zoom: 13,
  center: new google.maps.LatLng(42.31, -71.032), // boston
  minZoom: 10,
  maxZoom: 17,
  mapTypeControlOptions: {
      position: google.maps.ControlPosition.TOP_RIGHT,
      mapTypeIds: [bp.mapclayer, google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.SATELLITE], //,
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
  },
  panControl: false,
  zoomControlOptions: {
      style: google.maps.ZoomControlStyle.SMALL
  },
  streetViewControl: false
})

// add custom mapclayer
bp.map.mapTypes.set(bp.mapclayer, new google.maps.MAPCMapType(bp.mapclayer));
bp.map.setMapTypeId(bp.mapclayer);


$(function() {   

  // execute onload with global parameter specified in django template
  if ( bp.parkfilter ) bp.loadparks(bp.parkfilter, bp.mapconf);

  // tooltip whenever a facility icon is displayed in a list
  $(".facility-icon").tooltip();

});


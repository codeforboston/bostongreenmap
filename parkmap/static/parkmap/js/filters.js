function update_second_dropdown(search_type, filter_type, filter,value_key){
  /*
    Pass in:
      The type of the second box for search_type
      The type of the first box for filter_type;
      The value to filter on for filter
      The value_key is whether to use 'id' or 'slug'
  */
  //Set the first item in the dropdown box
   var out = '<option SELECTED value="">Select Your ';
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
     //probe the correct park url
     url:'/api/v1/'+search_type+'/?format=json&limit=1000&'+filter_type+'='+filter,
     //url:url,
     dataType:'json',
     success:function(json){
       $.each(json['objects'], function(key, obj) {
         //check whether the value returned is supposed to be an id or a slug.
         //Create the new item in the dropdown list.
         out+= '<option value="'+obj[value_key]+'">' + obj['name']+'</option>';
       });
       //replace the items in the dropdown list, and select the first element
       $("#neighborhood_"+search_type).html(out);
       $("#neighborhood_"+search_type).selectedIndex = 0;
     }
   });
}


function explore_filter_activities(neighborhood_slug,parktype_id){
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
}


function explore_filter_parkactivities(){
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

  activities = activities.join(",");
  $.ajax({
     //probe the correct park url
     url:'/api/v1/explorepark/?format=json&limit=1000&neighborhood='+neighborhood+'&parktype='+parktype+'&activity_ids='+activities,
     //url:url,
     dataType:'json',
     success:function(json){
       var out = "";
        $.each(json['objects'], function(key, obj) {
           //DO SOMETHING BETTER HERE USING THE DATA.
        out+= obj['name'] + " - " + obj['os_id']+'<br>';
       });
       $("#parklist").html(out);
     }
   });

    $.ajax({
     url:'/api/v1/explorefacility/?format=json&limit=1000&neighborhood='+neighborhood+'&parktype='+parktype+'&activity_ids='+activities,
     dataType:'json',
     success:function(json){
      var out = "";
       $.each(json['objects'], function(key, obj) {
          //DO SOMETHING BETTER HERE USING THE DATA.
          out += obj['name'] + " - " + obj['id']+'<br>';
       });
       $("#facilitylist").html(out);
     }
   });

}


function update_second_dropdown(search_type, filter_type, filter,value_key){
  /*
    Pass in:
      The type of the second box for search_type
      The type of the first box for filter_type;
      The value to filter on for filter
      The value_key is whether to use 'id' or 'slug'
  */
  //Set the first item in the dropdown box
   var out = '<option SELECTED value="----">Select Your ';
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

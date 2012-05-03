//used on explore page.
function update_parktype(neighborhood, idname, slug_or_id){
     //Set the first item in the dropdown box
     var out = '<option SELECTED value="----">Select Your Type</option>';
     $.ajax({
         //probe the correct park url
         url:'/api/v1/parktype/?format=json&limit=1000&neighborhood='+neighborhood,
         //url:url,
         dataType:'json',
         success:function(json){
             $.each(json['objects'], function(key, obj) {
                 //check whether the value returned is supposed to be an id or a slug.
                 var value = slug_or_id = 1 ? 'id' : 'slug';
                 //Create the new item in the dropdown list.
                 out+= '<option value="'+obj[value]+'">' +obj['name']+'</option>';
             });
             //replace the items in the dropdown list, and select the first element
             $("#"+idname).html(out);
             $("#"+idname).selectedIndex = 0;
         }
     });
}

function ajax_with_page(url){
     //coming soon.
}

//Used on play page
function update_neighborhood(activity,idname, slug_or_id){
     var out = '<option SELECTED VALUE="----">Select Your Neighborhood/Town</option>';
     $.ajax({
         url:'/api/v1/neighborhood/?format=json&activity='+activity,
         dataType:'json',
         success:function(json){
             $.each(json['objects'], function(key, obj) {
out+= '<option value="'+obj['slug']+'">' +obj['name']+'</option>';
             });
             $("#neighborhood_neighborhood").html(out);
             $("#neighborhood_neighborhood").selectedIndex = 0;
         }
     });
}



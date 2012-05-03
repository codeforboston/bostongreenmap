function update_parktype(neighborhood, idname, slug_or_id){
     //Set the first item in the dropdown box
     var out = '<option SELECTED value="----">Select Your Type</option>';
         url:'/api/v1/parktype/?format=json&limit=1000&neighborhood='+neighborhood,
     $.ajax({
         //probe the correct park url
         url:url,
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
    
}
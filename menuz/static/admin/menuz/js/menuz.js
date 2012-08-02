/* @projectDescription jQuery Serialize Anything - Serialize anything (and not just forms!)
 * @author Bramus! (Bram Van Damme)
 * @version 1.0
 * @website: http://www.bram.us/
 * @license : BSD
*/

(function($) {

    $.fn.serializeAnything = function() {

        var toReturn    = [];
        var els         = $(this).find(':input').get();

        $.each(els, function() {
            if (this.name && !this.disabled && (this.checked || /select|textarea/i.test(this.nodeName) || /text|hidden|password/i.test(this.type))) {
                var val = $(this).val();
                toReturn.push( encodeURIComponent(this.name) + "=" + encodeURIComponent( val ) );
            }
        });
        return toReturn.join("&").replace(/%20/g, "+");
    }
})(django.jQuery);

//-------------------------- end serialize enything --------------------------//

/* @description: Django-menuz Javascript
 * @author: Eka Putra
 * @version: 2.0
 * @website: http://balitechy.com/
 * @license : BSD
*/

// Activate Nested Sortable
function activate_sortable(){
	$( ".sortable" ).nestedSortable({
	        items: "li",
	        handle: 'div',
	        toleranceElement: '> div',
	        placeholder: 'placeholder',
            update: function(event, ui) {
                // this is the tricky part, since there's no direct connection between
                // sortable and menu ID in DB, we use "rel" attributes in "li" to hold the menu ID
                // and sent it to server when hierarchy changed.
                var parent_tag = $(ui.item).parent().parent().prop('tagName');
                var item_id = $(ui.item).attr('rel');
                
                if( parent_tag == 'LI'){ 
                    var parent_id = $(ui.item).parent().parent().attr('rel');
                }else{
                    var parent_id = '';
                }
                reorder_menu(item_id, parent_id);
            }
    });
}

// Load Menu item list via ajax
// afterajax finish, activate sortable
function load_menu(){
    $('.menu_items').load(window.reload_menuz, function(){
        activate_sortable();
    });
}


// On page load
$(function() {
    load_menu();
});

function reorder_menu(item_id, parent_id){
    $('.menu_loading').show();
    var menu = new Array();
    $('.menu_container .menu_item').each(function(){
        var id = $(this).attr('rel');
        menu.push(id);
    });

    //If menu empty, than don't reorder.
    if(menu.length > 0){
        var menu_str = menu.join(',');
        var data = {
            'csrfmiddlewaretoken': window.csrf_token,
            'order' : menu_str,
            'item_id': item_id,
            'parent_id' : parent_id
        }

        $.post(window.reorder_menuz, data, function(response){
            $('.menu_loading').hide();
            if(response.status !='success' ){
                alert(response.status);
            }
        },'json');
    }else{
        $('.menu_loading').hide();
    }
}

function set_error(mtype, fields){
    $('.menu_'+mtype).addClass('error');
    for(field in fields){
        $('#id_'+fields[field]).addClass('error');
    }
}

function reset_error(){
    $('.block_menu').removeClass('error');
    $('input').removeClass('error');
}

function reset_checkbox(){
    $('input[type=checkbox]').each(function(){
        $(this).attr('checked', false);
    });
}

function truncatechars_right(text, length){
  if (text.length > length) {
    return text.slice(0, length-3) + "...";
  } else {
    return text;
  }
}

function add_to_menu(mtype){
    reset_error();
    $('.menu_'+mtype+' img.loading').show();
    var formdata = django.jQuery('.menu_'+mtype).serializeAnything();
    $.post(window.add_menuz, formdata, function(response){
        $('.menu_'+mtype+' img.loading').hide();
        if(response.status == 'success'){
            load_menu();
            reset_checkbox();
        }else{
            set_error(mtype, response.fields)
        }
    }, 'json');
}

function delete_menu(mtype, item_id){
    $('.menu_loading').show();
    $.post(window.delete_menuz, {'csrfmiddlewaretoken': window.csrf_token, 'item_id': item_id}, function(response){
        $('.menu_loading').hide();
        if(response.status == 'success'){
            $('.menu_item.'+mtype+'_'+item_id).css('background','#cc3434').animate({opacity:0}, 500, function(){
                    $(this).parent().remove();
                    reorder_menu();
            });
        }
    }, 'json');
}

function toggle_menu_editor(mtype, item_id){
    $('.menu_editor.'+mtype+'_'+item_id).slideToggle('fast');
}

function filter(keyword, menu){
    $('.'+menu+' .block_content label').each(function(){
        if($(this).text().search(new RegExp(keyword, "i")) < 0){
            $(this).hide();
        }else{
            $(this).show();
        }
    });
}

/*--------- Update menu item----------*/

function input_error(input_parent){
    $('.'+input_parent+' input.vTextField').addClass('error');
}

function reset_input_error(input_parent){
    $('.menu_editor input.vTextField').removeClass('error');
}

function update_menu(type, item_id){
    $('img.loading_'+item_id).show();
    reset_input_error(type+'_'+item_id);

    var item_data = django.jQuery('.menu_editor.'+type+'_'+item_id).serializeAnything();
    $.post(window.update_menuz, item_data, function(response){
        $('img.loading_'+item_id).hide();
        if(response.status == 'success'){
            $('.menu_item.'+type+'_'+item_id+' .title').text(truncatechars_right(response.new_title, 40));
        }else{
            input_error(type+'_'+item_id);
        }
    },'json');
}

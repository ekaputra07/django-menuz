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

$(function() {
    //Drag and Drop actions
	$( ".menu_container" ).sortable({
	        items: " .menu_item:not(.ui-state-disabled)",
            stop: function(event, ui) {
                reorder_menu();
            }
    });

	//Menu Hover
    $('.menu_container .menu_item').hover(
        function(){
            $(this).addClass('hovered');
            },
        function(){
            $(this).removeClass('hovered');
            }
        );

});

function reorder_menu(){
    $('.menu_loading').show();
    var menu = new Array();
    $('.menu_container .menu_item').each(function(){
        var id = $(this).attr('rel');
        menu.push(id);
    });

    //If menu empty, than don't reorder.
    if(menu.length > 0){
        var menu_str = menu.join(',');
        data = {
            'csrfmiddlewaretoken': window.csrf_token,
            'order' : menu_str
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

function render_menu(menu_data){

    for(menu in menu_data){
        var menu_id = menu_data[menu]['id'];
        var title = truncatechars_right(menu_data[menu]['title'], 40);
        var title_value = menu_data[menu]['title'];
        var url = menu_data[menu]['url'];
        var content_type = menu_data[menu]['content_type'];
        var content_id = menu_data[menu]['content_id'];

        html = '\
        <div class="menu_item '+content_type+'_'+menu_id+'" rel="'+menu_id+'">\
        <h2><span class="move"></span>\
        <span class="title">'+title+'</span>\
        <a href="javascript:;" class="delete" title="Delete" onclick="delete_menu(\''+content_type+'\', '+menu_id+');"/></a>\
        <a href="javascript:;" class="edit" title="Edit" onclick="toggle_menu_editor(\''+content_type+'\', '+menu_id+');"/></a></h2>\
        <div class="menu_editor '+content_type+'_'+menu_id+'">\
        <!-- form -->\
        <input type="hidden" name="csrfmiddlewaretoken" value="'+window.csrf_token+'">\
        <input type="hidden" name="mtype" value="'+content_type+'">\
        <input type="hidden" name="item_id" value="'+menu_id+'">\
        <p>\
        <label for="id_'+content_type+'_title_'+menu_id+'">Title</label>\
        <input type="text" name="'+content_type+'_title_'+menu_id+'" id="id_'+content_type+'_title_'+menu_id+'" value="'+title_value+'" class="vTextField"/>\
        </p>';

        if(content_type == 'custom'){
            html += '<p>\
            <label for="id_'+content_type+'_url_'+menu_id+'">URL</label>\
            <input type="text" name="'+content_type+'_url_'+menu_id+'" id="id_'+content_type+'_url_'+menu_id+'" value="'+url+'" class="vTextField"/>\
            </p>';
        }

        html += '<p>\
        <input type="button" name="btn_update" value="Update" onclick="update_menu(\''+content_type+'\', '+menu_id+');"/>\
        <img src="'+window.__admin_media_prefix__+'menuz/images/loading.gif" class="menu_update_loading loading_'+menu_id+'"/>\
        </p>\
        <!-- enddform -->\
        </div>\
        </div>';

        $('.menu_container').append(html);
        reorder_menu();
    }
}

function add_to_menu(mtype){
    reset_error();
    $('.menu_'+mtype+' img.loading').show();
    var formdata = django.jQuery('.menu_'+mtype).serializeAnything();
    $.post(window.add_menuz, formdata, function(response){
        $('.menu_'+mtype+' img.loading').hide();
        if(response.status == 'success'){
            render_menu(response.menu_data);
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
                    $(this).remove();
                    reorder_menu();
            });
        }
    }, 'json');
}

function toggle_menu_editor(mtype, item_id){
    $('.menu_editor.'+mtype+'_'+item_id).slideToggle('fast');
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


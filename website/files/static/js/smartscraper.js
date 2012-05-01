jQuery(document).ready(function ($) {
    $(document).ajaxSend(function(event, xhr, settings) {
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
		    var cookie = jQuery.trim(cookies[i]);
		    // Does this cookie string begin with the name we want?
		    if (cookie.substring(0, name.length + 1) == (name + '=')) {
			cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			break;
		    }
		}
	    }
	    return cookieValue;
	}

	function sameOrigin(url) {
	    // url could be relative or scheme relative or absolute
	    var host = document.location.host; // host + port
	    var protocol = document.location.protocol;
	    var sr_origin = '//' + host;
	    var origin = protocol + sr_origin;
	    // Allow absolute or scheme relative URLs to same origin
	    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		// or any other URL that isn't scheme relative or absolute i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
	}

	function safeMethod(method) {
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
	    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
    });
    field_counter = 1
    $('#add_field').click(function() {
	$('#fields').append('<div id=field' + field_counter + '><div class="row"> <div class="two columns"><input type="text" placeholder="Name of Field" class="small input-text" id="field_name' + field_counter + '"/></div><div class="two columns"><a href="javascript:void(0);" class="nice small white button radius" id="delete_field' + field_counter + '">-</a></div><div class="eight columns"></div></div><div class="row"><div class="four columns"><textarea id="text_to_match' + field_counter + '" class="large_text_area" placeholder="Text to Match"></textarea></div><div class="two columns"><label for="ignorebreaks' + field_counter + '"><input type="checkbox" id="ignore_breaks' + field_counter + '" />Ignore Breaks</label></div><div class="six columns"></div></div></div>');
	var local_counter = field_counter
	$('#delete_field' + local_counter).click(function() {
	    $('#field_name'+ local_counter).remove();
	    $('#field' + local_counter).remove();
	});
	field_counter++;
    });


    $('#submit').click(function() {

	var json_data = {};
	json_data['url'] = $('#url').val();
	json_data['name'] = $('#name').val();
	fields = new Array();
	var counter = 0;
	var counter_array = 0
	while (counter < field_counter) {
	    if ($('#field_name' + counter).val() == undefined) {
		counter++;
		continue;
	    }
	    field = new Array();
	    field[0] = $('#field_name' + counter).val();
	    field[1] = $('#text_to_match' + counter).val();
	    field[2] = $('#ignore_breaks' + counter).is(':checked');
	    fields[counter_array]  = field;
	    counter++;
	    counter_array++;
	}
	json_data['fields'] = fields;
        var data = JSON.stringify(json_data);
        $.ajax({
            type: 'POST',
            dataType: 'text',
            url: '/submitEntry/',
            data: data,
            dataType: 'text',
            complete: function(res, status) {
		if (status == "success") {
                    window.location.href = '/get?id=' + res.responseText;
		} else {
		    alert("An error occured. Please try again");
		}
            }
        });
    });
    function getUrlVars() {
	var vars = {};
	var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
	});
	return vars;
    }
    $('#scrape').click(function() {
	var id = getUrlVars()["id"];
	var url = $('#scrape_url').val()
	$.get("/scrape", { id: id, url: url }, function(fields_string) {
	    var fields = eval('(' + fields_string + ')');
	    //alert(JSON.stringify(fields));
	    for(var field in fields) {
		if (fields[field] instanceof Array) {
		    $('#' + field).html("");
		    for (i in fields[field]) {
			f = fields[field][i];
			if (!f || f.toLowerCase() == "none") {
			    continue;
			}
			$('#' + field).append(f + "<br/>");
			
		    }
		} else {
		    $('#' + field).html(fields[field]);
		}
	    }
	});

    });
    

    $('#submit_multiple_match').click(function() {
	var json_data = {};
	json_data['url'] = $('#url').val();
	json_data['name'] = $('#name').val();
	fields = new Array();
	var counter = 0;
	var counter_array = 0
	while (counter < field_counter) {
	    if ($('#field_name' + counter).val() == undefined) {
		counter++;
		continue;
	    }
	    field = new Array();
	    field[0] = $('#field_name' + counter).val();
	    field[1] = $('#text_to_match' + counter).val();
	    field[2] = $('#ignore_breaks' + counter).is(':checked');
	    fields[counter_array]  = field;
	    counter++;
	    counter_array++;
	}
	json_data['fields'] = fields;
        var data = JSON.stringify(json_data);
        $.ajax({
            type: 'POST',
            dataType: 'text',
            url: '/submitMultiMatch/',
            data: data,
            dataType: 'text',
            success: function(g) {
		
                window.location.href = '/get?id=' + g;

            }
        });

    });

});

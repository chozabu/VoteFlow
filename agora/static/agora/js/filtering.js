function getfilteritem(achild){
    var mainbox = $(this).parentsUntil(".filteritem");
    if (mainbox.length == 0){
        console.log(achild.parent());
        return achild.parent();
        }
    console.log(mainbox.parent());
    return mainbox.parent();

}
function postfilterbox_changed(event){
    console.log("---")
    console.log($(this));
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    console.log(newval);
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
    var tagbox = mainbox.find('#tagfilterbox');
    console.log(floatbox);
    if( $.inArray( newval, [ "liquid_value", "liquid_sum",
    "direct_value", "direct_sum" ] ) != -1){
        floatbox.show();
        datebox.hide();
        strbox.hide();
        tagbox.hide();
    }
    if( $.inArray( newval, [ "name", "text" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.show();
        tagbox.hide();
    }
    if( $.inArray( newval, [ "created_at" ] ) != -1){
        floatbox.hide();
        datebox.show();
        strbox.hide();
        tagbox.hide();
    }
    if( $.inArray( newval, [ "tag" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.hide();
        tagbox.show();
        console.log("doing TAG change")
        tagbox.find('#tagfilterbox').change();
        $('#tagfilterbox').change();
        console.log("doing TAG change")
    }
}
function tagfilterbox_changed(event){
    //floatbox.hide();
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
    var tagbox = mainbox.find('#tagfilterbox');
    console.log(newval);
    if( $.inArray( newval, [ "liquid_value", "liquid_sum",
    "direct_value", "direct_sum" ] ) != -1){
        floatbox.show();
        datebox.hide();
        strbox.hide();
    }
    else if( $.inArray( newval, [ "name", "text" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.show();
    }
    else if( $.inArray( newval, [ "created_at" ] ) != -1){
        floatbox.hide();
        datebox.show();
        strbox.hide();
    }
}
function setout(val){
    console.log(val);
    $('#outbox')[0].textContent=val;
}
function get_filters(fcontainername, fboxname){
    var fbox = $(fcontainername).find(fboxname).children();
    var filters = [];
    for (var fi = 0;fi<fbox.length;fi++){
        //console.log("loop");
        //console.log(fbox[fi]);
        //console.log($(fbox[fi]));
        filters.push(get_filter($(fbox[fi])));
    }
    //console.log(filters);
    return filters;
    //  mainbox.find('#outbox')[0].textContent=JSON.stringify(filter);
}
function print_filter(event){
    var mainbox = $(this).parent().parent()
    filter = get_filter(mainbox);
    console.log(filter);
    mainbox.find('#outbox')[0].textContent=JSON.stringify(filter);
}
function get_filter(mainbox){
    console.log("mainbox");
    console.log(mainbox);
    console.log(mainbox.find('#postfilterbox'));

    var first = mainbox.find('#postfilterbox')[0].value;
    if( $.inArray( first, [ "liquid_value", "liquid_sum",
    "direct_value", "direct_sum" ] ) != -1){
        var second = mainbox.find('#floatfilterbox')[0].value;
        var filterval = mainbox.find('#floatfilterval')[0].value;
    }
    else if( $.inArray( first, [ "name", "text" ] ) != -1){
        var second = mainbox.find('#strfilterbox')[0].value;
        var filterval = mainbox.find('#strfilterval')[0].value;
    }
    else if( $.inArray( first, [ "created_at" ] ) != -1){
        var second = mainbox.find('#datefilterbox')[0].value;
        var filterval = mainbox.find('#datefilterval')[0].value;
    }
    else if( $.inArray( first, [ "tag" ] ) != -1){
        var second = mainbox.find('#tagfilterbox')[0].value;
        //var filterval = mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "liquid_value", "liquid_sum",
        "direct_value", "direct_sum" ] ) != -1){
            var third = mainbox.find('#floatfilterbox')[0].value;
            var filterval = mainbox.find('#floatfilterval')[0].value;
        }
        else if( $.inArray( second, [ "name", "text" ] ) != -1){
            var third = mainbox.find('#strfilterbox')[0].value;
            var filterval = mainbox.find('#strfilterval')[0].value;
        }
        else if( $.inArray( second, [ "created_at" ] ) != -1){
            var third = mainbox.find('#datefilterbox')[0].value;
            var filterval = mainbox.find('#datefilterval')[0].value;
        }
        rval = {}
        if (third=="")
            rval[first+"__"+second]=filterval;
        else
            rval[first+"__"+second+"__"+third]=filterval;
        return rval;
    }
    else {
        rval = {}
        rval[first]="?";
        return rval;
    }
    rval = {}
    rval[first+"__"+second]=filterval
    return rval;
}

$('#check').click(print_filter);
$('#postfilterbox').change(postfilterbox_changed);
$('#tagfilterbox').change(tagfilterbox_changed);


function new_filter(event){
    new_filter_action('#currentfiltersbox');
}
function new_exclude(event){
    new_filter_action('#currentexcludesbox');
}

function new_filter_action(foe){
    console.log("new filter");
    console.log($('#filterproto'));
    var newfilter = $('#filterproto').clone(true);
    newfilter.find('#postfilterbox').change();
    newfilter[0].id="afilter";
    newfilter.show();
    $(foe).append(newfilter);
}
function new_filter_from_json(jin){
    console.log("new filter");
    console.log($('#filterproto'));
    //get the key and value object
    //split key by __s?
    //same structure as getfilter, but setting values
    var newfilter = $('#filterproto').clone(true);
    newfilter.find('#postfilterbox').change();
    newfilter[0].id="afilter";
    newfilter.show();
    $('#currentfiltersbox').append(newfilter);
}
$('#newfilterbutton').click(new_filter);
$('#newexcludebutton').click(new_exclude);
$('#filterproto').hide();
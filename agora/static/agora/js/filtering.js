function getfilteritem(achild){
    var mainbox = $(this).parentsUntil(".filteritem");
    if (mainbox.length == 0){
        //console.log(achild.parent());
        return achild.parent();
        }
    //console.log(mainbox.parent());
    return mainbox.parent();

}
/*
nextbox = {
    "name": "strfiltercontainer",
    "text": "strfiltercontainer",
    "author": "strfiltercontainer",
    "liquid_value": "strfiltercontainer",
    "liquid_sum": "strfiltercontainer",
    "created_at": "strfiltercontainer",
    "direct_value": "strfiltercontainer",
    "direct_sum": "strfiltercontainer",
    "tag": "strfiltercontainer",
    "group": "strfiltercontainer",
    "topic": "strfiltercontainer",
    "parent": "strfiltercontainer",
    "id": "strfiltercontainer"
    }
*/
function postfilterbox_changed(event){
    //console.log("---")
    //console.log($(this));
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    //console.log(newval);
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
    var tagbox = mainbox.find('#tagfilterbox');
    var topicbox = mainbox.find('#topicfilterbox');
    var groupbox = mainbox.find('#groupfilterbox');
    var parentbox = mainbox.find('#parentfilterbox');
    //console.log(floatbox);
    if( $.inArray( newval, [ "liquid_value", "liquid_sum",
    "direct_value", "direct_sum" ] ) != -1){
        floatbox.show();
        datebox.hide();
        strbox.hide();
        tagbox.hide();
        topicbox.hide();
        groupbox.hide();
        parentbox.hide();
    }
    if( $.inArray( newval, [ "name", "text" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.show();
        tagbox.hide();
        topicbox.hide();
        groupbox.hide();
        parentbox.hide();
    }
    if( $.inArray( newval, [ "created_at" ] ) != -1){
        floatbox.hide();
        datebox.show();
        strbox.hide();
        tagbox.hide();
        topicbox.hide();
        groupbox.hide();
        parentbox.hide();
    }
    if( $.inArray( newval, [ "tag" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.hide();
        tagbox.show();
        topicbox.hide();
        groupbox.hide();
        parentbox.hide();
        //console.log("doing TAG change")
        tagbox.trigger('change');
        //console.log("done TAG change")
    }
    if( $.inArray( newval, [ "topic" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.hide();
        tagbox.hide();
        topicbox.show();
        groupbox.hide();
        parentbox.hide();
        //console.log("doing topic change")
        topicbox.trigger('change');
        //console.log("done topic change")
    }
    if( $.inArray( newval, [ "group" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.hide();
        tagbox.hide();
        topicbox.hide();
        groupbox.show();
        parentbox.hide();
        //console.log("doing group change")
        groupbox.trigger('change');
        //console.log("done group change")
    }
    if( $.inArray( newval, [ "parent" ] ) != -1){
        floatbox.hide();
        datebox.hide();
        strbox.hide();
        tagbox.hide();
        topicbox.hide();
        groupbox.hide();
        parentbox.show();
        //console.log("doing parent change")
        parentbox.trigger('change');
        //console.log("done parent change")
    }
}
function tagfilterbox_changed(event){
    //console.log("TFT")
    //floatbox.hide();
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
    var tagbox = mainbox.find('#tagfilterbox');
    //console.log(newval);
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
function topicfilterbox_changed(event){
    //console.log("TFT")
    //floatbox.hide();
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
    //console.log(newval);
    if( $.inArray( newval, [ "id" ] ) != -1){
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
function groupfilterbox_changed(event){
    //console.log("TFT")
    //floatbox.hide();
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
    //console.log(newval);
    if( $.inArray( newval, [ "id" ] ) != -1){
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
function parentfilterbox_changed(event){
    //console.log("TFT")
    //floatbox.hide();
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
    console.log(newval);
    if( $.inArray( newval, [ "id", "", null ] ) != -1){
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
    //console.log(val);
    $('#outbox')[0].textContent=val;
}
function get_filters(fcontainername, fboxname){
    var fbox = $(fcontainername).find(fboxname).children();
    var filters = [];
    for (var fi = 0;fi<fbox.length;fi++){
        ////console.log("loop");
        ////console.log(fbox[fi]);
        ////console.log($(fbox[fi]));
        filters.push(get_filter($(fbox[fi])));
    }
    ////console.log(filters);
    return filters;
    //  mainbox.find('#outbox')[0].textContent=JSON.stringify(filter);
}
function remove_filter(event){
    $(this).parent().remove();
}
function print_filter(event){
    var mainbox = $(this).parent().parent()
    filter = get_filter(mainbox);
    //console.log(filter);
    mainbox.find('#outbox')[0].textContent=JSON.stringify(filter);
}
function get_filter(mainbox){
    //console.log("mainbox");
    //console.log(mainbox);
    //console.log(mainbox.find('#postfilterbox'));

    var first = mainbox.find('#postfilterbox')[0].value;
        //console.log("!!!!asd!!!!!")
        //console.log("!!!!!!!!!", first)
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
    else if( $.inArray( first, [ "topic" ] ) != -1){
        var second = mainbox.find('#topicfilterbox')[0].value;
        //var filterval = mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "id", "" ] ) != -1){
            var third = mainbox.find('#floatfilterbox')[0].value;
            var filterval = mainbox.find('#floatfilterval')[0].value;
            if (filterval == "") filterval = null;
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
    else if( $.inArray( first, [ "group" ] ) != -1){
        var second = mainbox.find('#groupfilterbox')[0].value;
        //var filterval = mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "id", "" ] ) != -1){
            var third = mainbox.find('#floatfilterbox')[0].value;
            var filterval = mainbox.find('#floatfilterval')[0].value;
            if (filterval == "") filterval = null;
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
    else if( $.inArray( first, [ "parent" ] ) != -1){
        var second = mainbox.find('#parentfilterbox')[0].value;
        //var filterval = mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "id", "" ] ) != -1){
            var third = mainbox.find('#floatfilterbox')[0].value;
            var filterval = mainbox.find('#floatfilterval')[0].value;
            if (filterval == "") filterval = null;
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
function set_filter(mainbox, items, value){
    //console.log("##########DEBUG LVAL#######");
    //console.log("mainbox");
    //console.log(mainbox);
    //console.log(mainbox.find('#postfilterbox'));

    //console.log("ITEMS:", items, items.length)
    var first = items[0];
    var second = "";
    var third = "";
    if (items.length>1)
        second = items[1];
    if (items.length>2)
        third = items[2];
    //console.log("ITEMS:", first, second, third)

    mainbox.find('#postfilterbox')[0].value = first;
    mainbox.find('#postfilterbox').trigger('change');
    if( $.inArray( first, [ "liquid_value", "liquid_sum",
    "direct_value", "direct_sum" ] ) != -1){
        mainbox.find('#floatfilterbox')[0].value = second;
        mainbox.find('#floatfilterval')[0].value = value;
    }
    else if( $.inArray( first, [ "name", "text" ] ) != -1){
        mainbox.find('#strfilterbox')[0].value = second;
        mainbox.find('#strfilterval')[0].value = value;
    }
    else if( $.inArray( first, [ "created_at" ] ) != -1){
        mainbox.find('#datefilterbox')[0].value = second;
        mainbox.find('#datefilterval')[0].value = value;
    }
    else if( $.inArray( first, [ "tag" ] ) != -1){
        mainbox.find('#tagfilterbox')[0].value = second;
        mainbox.find('#tagfilterbox').trigger('change');
        //mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "liquid_value", "liquid_sum",
        "direct_value", "direct_sum" ] ) != -1){
            mainbox.find('#floatfilterbox')[0].value = third;
            mainbox.find('#floatfilterval')[0].value = value;
        }
        else if( $.inArray( second, [ "name", "text" ] ) != -1){
            mainbox.find('#strfilterbox')[0].value = third;
            mainbox.find('#strfilterval')[0].value = value;
        }
        else if( $.inArray( second, [ "created_at" ] ) != -1){
            mainbox.find('#datefilterbox')[0].value = third;
            mainbox.find('#datefilterval')[0].value = value;
        }
    }
    else if( $.inArray( first, [ "topic" ] ) != -1){
        mainbox.find('#topicfilterbox')[0].value = second;
        mainbox.find('#topicfilterbox').trigger('change');
        //mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "id" ] ) != -1){
            mainbox.find('#floatfilterbox')[0].value = third;
            mainbox.find('#floatfilterval')[0].value = value;
        }
        else if( second == ""){
            mainbox.find('#floatfilterbox')[0].value = "";
            mainbox.find('#floatfilterval')[0].value = value;
        }
        else if( $.inArray( second, [ "name", "text" ] ) != -1){
            mainbox.find('#strfilterbox')[0].value = third;
            mainbox.find('#strfilterval')[0].value = value;
        }
        else if( $.inArray( second, [ "created_at" ] ) != -1){
            mainbox.find('#datefilterbox')[0].value = third;
            mainbox.find('#datefilterval')[0].value = value;
        }
    }
    else if( $.inArray( first, [ "group" ] ) != -1){
        mainbox.find('#groupfilterbox')[0].value = second;
        mainbox.find('#groupfilterbox').trigger('change');
        //mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "id" ] ) != -1){
            mainbox.find('#floatfilterbox')[0].value = third;
            mainbox.find('#floatfilterval')[0].value = value;
        }
        else if( second == ""){
            mainbox.find('#floatfilterbox')[0].value = "";
            mainbox.find('#floatfilterval')[0].value = value;
        }
        else if( $.inArray( second, [ "name", "text" ] ) != -1){
            mainbox.find('#strfilterbox')[0].value = third;
            mainbox.find('#strfilterval')[0].value = value;
        }
        else if( $.inArray( second, [ "created_at" ] ) != -1){
            mainbox.find('#datefilterbox')[0].value = third;
            mainbox.find('#datefilterval')[0].value = value;
        }
    }
    else if( $.inArray( first, [ "parent" ] ) != -1){
        console.log("second: ",second);
        console.log("second: ",second=="");
        console.log("second: ",second==null);
        mainbox.find('#parentfilterbox')[0].value = second;
        mainbox.find('#parentfilterbox').trigger('change');
        //mainbox.find('#datefilterval')[0].value;
        //setout(first+second:filterval};
        if( $.inArray( second, [ "id" ] ) != -1){
            mainbox.find('#floatfilterbox')[0].value = third;
            mainbox.find('#floatfilterval')[0].value = value;
        }
        else if( second == ""){
            console.log("isemptsty")
            mainbox.find('#parentfilterbox')[0].value = "id";
            mainbox.find('#floatfilterbox')[0].value = third;
            mainbox.find('#floatfilterval')[0].value = value;
            //console.log(efpwnef)
        }
        else if( $.inArray( second, [ "name", "text" ] ) != -1){
            mainbox.find('#strfilterbox')[0].value = third;
            mainbox.find('#strfilterval')[0].value = value;
        }
        else if( $.inArray( second, [ "created_at" ] ) != -1){
            mainbox.find('#datefilterbox')[0].value = third;
            mainbox.find('#datefilterval')[0].value = value;
        }
        //console.log("ASDASD")
    }
}

$('#check').click(print_filter);
$('#removefilter').click(remove_filter);
$('#postfilterbox').change(postfilterbox_changed);
$('#tagfilterbox').change(tagfilterbox_changed);
$('#topicfilterbox').change(topicfilterbox_changed);
$('#groupfilterbox').change(groupfilterbox_changed);
$('#parentfilterbox').change(parentfilterbox_changed);


function new_filter(event){
    new_filter_action('#currentfiltersbox');
}
function new_exclude(event){
    new_filter_action('#currentexcludesbox');
}

function new_filter_action(foe){
    //console.log("new filter");
    //console.log($('#filterproto'));
    var newfilter = $('#filterproto').clone(true);
    newfilter.find('#postfilterbox').change();
    newfilter[0].id="afilter";
    newfilter.show();
    $(foe).append(newfilter);
    return newfilter;
}
function new_filter_from_json(jin, foe){
    //console.log("new filter");
    //console.log($('#filterproto'));
    foe = '#currentfiltersbox';
    newfilter = new_filter_action(foe);
    //get the key and value object
    var query = "";
    var val = "";
    for (k in jin){
        query=k;
        val=jin[k];
    }
    //split key by __s?
    var qparts = query.split("__");
    set_filter(newfilter, qparts, val);
    //same structure as getfilter, but setting values
}
$('#newfilterbutton').click(new_filter);
$('#newexcludebutton').click(new_exclude);
$('#filterproto').hide();
function getfilteritem(achild){
    var mainbox = $(this).parentsUntil(".ruleitem");
    if (mainbox.length == 0){
        //console.log(achild.parent());
        return achild.parent();
        }
    //console.log(mainbox.parent());
    return mainbox.parent();

}function getrealfilteritem(achild){
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

function presetfilters_changed(event){
    var newfilterstr = $(this)[0].value;
    var mainbox = getfilteritem($(this));
    set_filter_from_json(JSON.parse(newfilterstr), mainbox);
}
function parentfilterbox_changed(event){
    //console.log("TFT")
    //floatbox.hide();
    var mainbox = getfilteritem($(this))
    var newval = $(this)[0].value;
    var floatbox = mainbox.find('#floatfiltercontainer');
    var datebox = mainbox.find('#datefiltercontainer');
    var strbox = mainbox.find('#strfiltercontainer');
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
function clear_filters(fcontainername, fboxname){
    var fbox = $(fcontainername).find(fboxname).children();
    fbox.remove();
}
function get_filters(fcontainername, fboxname){
    var fbox = $(fcontainername).find(fboxname).children();
    var filters = [];
    for (var fi = 0;fi<fbox.length;fi++){
        ////console.log("loop");
        ////console.log(fbox[fi]);
        ////console.log($(fbox[fi]));
        filters.push(get_rules($(fbox[fi])));
    }
    ////console.log(filters);
    return filters;
    //  mainbox.find('#outbox')[0].textContent=JSON.stringify(filter);
}
function remove_filter(event){
    $(this).parent().remove();
}
function print_filter(event){
    console.log("printing filter")
    var mainbox = $(this).parent().parent()
    console.log(mainbox);
    filter = get_filter(mainbox);
    console.log(filter);
    mainbox.find('#outbox')[0].textContent=JSON.stringify(filter);
}
function print_filters(event){
    console.log("printing filter")
    var mainbox = $(this).parent();
    filters = get_rules(mainbox);
    console.log(filters)
}
function get_rules(mainbox){
    filters = []
    //console.log(mainbox);
    var rulesdiv = mainbox.find('#postfilterrules');
    //console.log(rulesdiv);
    //console.log(rulesdiv.children());
    rulesdiv.children().each(function() {
      filters.push(get_filter($( this )))
    })
    rules = {}
    for (f in filters){
        fi = filters[f]
        for (fin in fi){
        rules[fin]=fi[fin];
        }
    }
    console.log("rules:",JSON.stringify(rules))
    return rules;

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
function set_filter(mainbox, query, value){
    var items = query.split("__");
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
$('#checkall').click(print_filters);
$('#removefilter').click(remove_filter);
$('#postfilterbox').change(postfilterbox_changed);
$('#tagfilterbox').change(tagfilterbox_changed);
$('#topicfilterbox').change(topicfilterbox_changed);
$('#groupfilterbox').change(groupfilterbox_changed);
$('#parentfilterbox').change(parentfilterbox_changed);
$('#presetfilters').change(presetfilters_changed);


function new_filter(event){
    new_filter_action('#currentfiltersbox');
}
function new_exclude(event){
    new_filter_action('#currentexcludesbox');
}


function new_rule(event){
    var filter = $(this).parent();
    new_rule_on(filter);
}

function new_rule_on(filter){
    var rules = filter.find('#postfilterrules');
    var newrule = $('#postfilterpair').clone(true);
    rules.append(newrule);
    newrule.find('#postfilterbox').trigger('change');
    return newrule;
}
function new_rule_action(ruleitem){
    //console.log("new filter");
    //console.log($('#filterproto'));
    var newfilter = $('#filterproto').clone(true);
    newfilter.find('#postfilterbox').change();
    newfilter[0].id="afilter";
    newfilter.show();
    $(foe).append(newfilter);
    $('#newrulebutton').click(new_rule);
    return newfilter;
}

function new_filter_action(foe){
    //console.log("new filter");
    //console.log($('#filterproto'));
    var newfilter = $('#filterproto').clone(true);
    newfilter.find('#postfilterbox').change();
    newfilter[0].id="afilter";
    newfilter.show();
    $(foe).append(newfilter);
    $('#newrulebutton').click(new_rule);
    return newfilter;
}
function set_filters_from_json(jin){
    $("#currentfiltersbox").children().remove();
    var filters = JSON.parse(jin);
    console.log("FILTERS!!!!!!!\n\n")
    console.log(filters, "\n\n")
    for (var j in filters){
        new_filter_from_json(filters[j], "#currentfiltersbox")
    }
}
function set_excludes_from_json(jin){
    $("#currentexcludesbox").children().remove();
    var filters = JSON.parse(jin);
    for (var j in filters){
        new_filter_from_json(filters[j], "#currentexcludesbox")
    }
}
function new_exclude_from_json(jin){
    new_filter_from_json(jin, "#currentexcludesbox")
}
function new_filter_from_json(jin, foe){
    if (foe==undefined)foe = '#currentfiltersbox';
    newfilter = new_filter_action(foe);
    //get the key and value object

    var query = "";
    var val = "";
    a=newfilter.find('#postfilterpair')
    var first = true;
    for (k in jin){
        query=k;
        val=jin[k];
        if (first==false) a=new_rule_on(newfilter);
        set_filter(a, query, val);
        first = false;
    }
    //split key by __s?
    //same structure as getfilter, but setting values

    var rootbox = $(foe);
    var psf = rootbox.find('#presetfilters');
    console.log("SETTING FILTER",JSON.stringify(jin))
    psf[0].value=JSON.stringify(jin);

}
function set_filter_from_json(jin, filterbox){
    var query = "";
    var val = "";
    filterbox.find('#postfilterpair').remove()
    var first = true;
    for (k in jin){
        query=k;
        val=jin[k];
        a=new_rule_on(filterbox);
        set_filter(a, query, val);
        first = false;
    }
    //split key by __s?
    //same structure as getfilter, but setting values
}
$('#newfilterbutton').click(new_filter);
$('#addrule').click(new_rule);
$('#newexcludebutton').click(new_exclude);
$('#filterproto').hide();
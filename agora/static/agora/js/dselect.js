function getdselectitem(achild){
    var mainbox = $(this).parentsUntil(".ruleitem");
    if (mainbox.length == 0){
        //console.log(achild.parent());
        return achild.parent();
        }
    //console.log(mainbox.parent());
    return mainbox.parent();

}
function getrealdselectitem(achild){
    var mainbox = $(this).parentsUntil(".dselectitem");
    if (mainbox.length == 0){
        //console.log(achild.parent());
        return achild.parent();
        }
    //console.log(mainbox.parent());
    return mainbox.parent();

}

function postdselectbox_changed(event){
    //console.log("---")
    //console.log($(this));
    var mainbox = getdselectitem($(this))
    var newval = $(this)[0].value;
    //console.log(newval);
    var tagbox = mainbox.find('#tagselectcontainer');
    //console.log(floatbox);
    if( $.inArray( newval, [ "tag" ] ) != -1){
        tagbox.show();
    } else {
        tagbox.hide();
    }
}

function get_dselects(fcontainername){
    var fbox = $(fcontainername).children();
    return get_dselect(fbox);
}
function set_dselects(fcontainername, query){
    var fbox = $(fcontainername).children();
    return set_dselect(fbox, query);
}
function print_dselect(event){
    console.log("printing dselect")
    var mainbox = $(this).parent().parent()
    console.log(mainbox);
    dselect = get_dselect(mainbox);
    console.log(dselect);
    mainbox.find('#outbox')[0].textContent=JSON.stringify(dselect);
}


function get_dselect(mainbox){
    //console.log("mainbox");
    //console.log(mainbox);
    //console.log(mainbox.find('#postdselectbox'));

    var first = mainbox.find('#postdselectbox')[0].value;
    if( $.inArray( first, [ "tag" ] ) != -1){
        var second = mainbox.find('#tagnamebox')[0].value;
        var third = mainbox.find('#tagdselectbox')[0].value;
        return first+"__"+second+"__"+third;
    }
    return first;
}
function set_dselect(mainbox, query){
    var items = query.split("__");
    //console.log("##########DEBUG LVAL#######");
    //console.log("mainbox");
    //console.log(mainbox);
    //console.log(mainbox.find('#postdselectbox'));

    console.log("ITEMS:", items, items.length)
    var first = items[0];
    var second = "";
    var third = "";
    if (items.length>1)
        second = items[1];
    if (items.length>2)
        third = items[2];
    //console.log("ITEMS:", first, second, third)

    mainbox.find('#postdselectbox')[0].value = first;
    mainbox.find('#postdselectbox').trigger('change');
    if( $.inArray( first, [ "tag" ] ) != -1){
        mainbox.find('#tagdselectbox')[0].value = second;
        mainbox.find('#tagdselectbox').trigger('change');
    }
}

//$('#postdselectbox').change(postdselectbox_changed);



function new_dselect_action(foe){
    //console.log("new dselect");
    //console.log($('#dselectproto'));
    var newdselect = $('#dselectproto').clone(true);
    newdselect.find('#postdselectbox').change();
    newdselect[0].id="adselect";
    newdselect.show();
    $(foe).append(newdselect);
    $('#newrulebutton').click(new_rule);
    return newdselect;
}

function new_dselect_from_json(jin, foe){
    if (foe==undefined)foe = '#currentdselectsbox';
    newdselect = new_dselect_action(foe);
    //get the key and value object

    var query = "";
    var val = "";
    a=newdselect.find('#postdselectpair')
    var first = true;
    for (k in jin){
        query=k;
        val=jin[k];
        if (first==false) a=new_rule_on(newdselect);
        set_dselect(a, query, val);
        first = false;
    }
    //split key by __s?
    //same structure as getdselect, but setting values

    var rootbox = $(foe);
    var psf = rootbox.find('#presetdselects');
    console.log("SETTING dselect",JSON.stringify(jin))
    psf[0].value=JSON.stringify(jin);

}
function set_dselect_from_json(jin, dselectbox){
    var query = "";
    var val = "";
    dselectbox.find('#postdselectpair').remove()
    var first = true;
    for (k in jin){
        query=k;
        val=jin[k];
        a=new_rule_on(dselectbox);
        set_dselect(a, query, val);
        first = false;
    }
    //split key by __s?
    //same structure as getdselect, but setting values
}

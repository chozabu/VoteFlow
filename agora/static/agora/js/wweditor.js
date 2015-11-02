var hallosettings = {
                plugins: {
                    'halloformat': {},
                    'halloheadings': {},
                    'hallolists': {},
                    //'halloblacklist': {"tags":["div"]},
                    'hallo-image-insert-edit': {},
                    'hallolink': {},
                    'halloreundo': {},
                    'hallocleanhtml': {
                      format: false,
                      allowedTags: [
                        'p',
                        'em',
                        'strong',
                        'br',
                        'h1',
                        'h2',
                        'h3',
                        'h4',
                        'ol',
                        'ul',
                        'li',
                        'img',
                        'a'],
                      allowedAttributes: ['style']
                    }
				},
                toolbar: 'halloToolbarFixed'
            }

var markdownize = function (content) {
    var html = content.split("\n").map($.trim).filter(function (line) {
        return line != "";
    }).join("\n");
    //next line for chrome...
    html = html.replace(/\<div\>/g, "<br>").replace(/\<\/div\>/g, "");
    return toMarkdown(html);
    /*md= toMarkdown(html);
    md = md.replace(/\&lt\;/g, "<");
    md = md.replace(/\&gt\;/g, ">");
    md = md.replace(/\&nbsp\;/g, "\ \ \n");
    md = md.replace(/\n/g, "\ \ \n");
    return md;*/
};



var converter = new Showdown.converter();
var htmlize = function (content) {
    return converter.makeHtml(content);
};
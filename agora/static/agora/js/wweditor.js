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
    //console.log(html)
    return toMarkdown(html);
};



var converter = new Showdown.converter();
var htmlize = function (content) {
    return converter.makeHtml(content);
};

function castvote(item){
	console.log("---castvote----");
	console.log(item);
	console.log($(this));
	var votelink = $(item)[0]
	var voteint = parseInt(votelink.getAttribute("vval"));
	var perc = (voteint)/6.0*100.0;
	console.log(perc);

	var pid = parseInt(item.parentNode.getAttribute("postid"));
	console.log(pid);

	$.post( "/agora/posts/"+pid+"/quickvote/", {
			"voteslider":perc
		}, function( data ) {
		location.reload();
	});
}



function link_as_post_reload(event){
    $.post( $(this)[0].getAttribute("plink"), {
        }, function( data ) {
      location.reload();
    });
}

jQuery(document).ready(function () {
	$('.link_as_post_reload').click(link_as_post_reload);
});
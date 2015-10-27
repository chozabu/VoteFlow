
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

	$.post( "/agora/posts/"+pid+"/easyvote/", {
			"voteslider":perc
		}, function( data ) {
		location.reload();
	});
}
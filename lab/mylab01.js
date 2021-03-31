

var task =  function(request, callback){
	var name = request.query.name ? request.query.name : "World";
	callback(null, "Hello, " + name + "!");
}

exports.lab = task
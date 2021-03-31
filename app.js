var lab1_1 = require("./lab/lab1_1").lab
var example_1 = require("./example_1").lab;
var mylab01 = require("./lab/mylab01").lab;

var PORT = 8080;


var urlMap = [
	{path: "/", action:__dirname + "/static/index.html"},	 
	{path: "/digest", action: lab1_1},	
	{path: "/example_1", action: example_1}, 
	{path: "/lab01", action: mylab01}, 
	];

var service = require("./lib/service").http(urlMap);

service(PORT);


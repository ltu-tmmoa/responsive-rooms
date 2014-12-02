var restify = require("restify");

// Creates a new Restify server.
var server = restify.createServer();

// This adds query information to the 'req' variable in resource handles.
server.use(restify.queryParser());

// Registers sensor, actuator and program resource handles.
require("./handlers/sensors.js").register(server);
require("./handlers/actuators.js").register(server);
require("./handlers/programs.js").register(server);

// Starts Restify server.
server.listen(14003);


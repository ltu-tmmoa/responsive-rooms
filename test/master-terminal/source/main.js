var restify = require("restify");

// Creates a new Restify server.
var server = restify.createServer();

// This adds query information to the 'req' variable in resource handles.
server.use(restify.queryParser());

// Registers sensor, actuator and program resource handles.
require("./handlers/sensors.js").register(server, reportError);
require("./handlers/actuators.js").register(server, reportError);
require("./handlers/programs.js").register(server, reportError);

// Starts Restify server.
server.listen(14003);

// Whenever an error is reported, this variable is increased.
var errors = 0;

// Error reporting function. All handlers use this to report on errors found
// while handling requests.
function reportError(message) {
    console.log("!! " + message);
    errors += 1;
}



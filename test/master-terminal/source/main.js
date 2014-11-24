var restify = require("restify");
var sensors = require("./handlers/sensors.js");
var actuators = require("./handlers/actuators.js");
var programs = require("./handlers/programs.js");

// Creates a new Restify server.
var server = restify.createServer();

// This adds query information to 'req' variable in resource handles.
server.use(restify.queryParser());

// Registers sensor, actuator and program resource handles.
sensors.register(server, reportError);
actuators.register(server, reportError);
programs.register(server, reportError);

// Starts Restify server.
server.listen(14003);

// Whenever an error is reported, this variable is increased.
var errors = 0;
function reportError(message) {
    console.log("!! " + message);
    errors += 1;
}

// The mock-up serivce lives for 500 ms before it dies. The service only exits
// with status 0 if no errors were reported.
setTimeout(function () {
    process.exit(errors);
}, 500);


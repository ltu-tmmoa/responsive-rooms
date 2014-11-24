var restify = require("restify");

// Creates a new Restify server.
var server = restify.createServer();

// These are the programs kept track of by the mock-up master service. They are
// not persistent as that would go against the purpose of having a mock-up.
var programs = {
    "temp_alarm.lua": "--[[Some lua code.]]--",
    "temp_monitor.lua": "--[[Some more lua code.]]--",
};

server.head("/programs", function (req, res, next) {
    if (req.headers["accept"] !== "application/lua") {
        reportError("'HEAD /programs' requires 'Accept: application/lua'.");
    }
    res.writeHead(200, {
        "Content-Type": "application/lua",
        "Content-Length": 0,
        "Collection-Items": Object.keys(programs).join(","),
    });
    res.end();

    next();
});

server.post("/programs", function (req, res, next) {
    if (req.headers["accept"] !== "text/plain") {
        reportError("'POST /programs' requires 'Accept: text/plain'.");
    }
    if (req.headers["content-type"] !== "application/lua") {
        reportError("'POST /programs' requires 'Content-Type: application/lua'.");
    }

    var name = req.headers["collection-item"];

    if (!name) {
        res.writeHead(400, {
            "Content-Type": "text/plain",
        });
        res.write("No program name given in message header.");
        res.end();

    } else if (programs[name]) {
        res.writeHead(403, {
            "Content-Type": "text/plain",
        });
        res.write("A program with that name already exists.");
        res.end();

    } else {
        req.on("data", function (data) {
            programs[name] = data.toString();
            res.writeHead(200, {
                "Content-Type": "text/plain",
                "Location": "/programs/" + name,
                "Content-Length": name.length,
            });
            res.write(name);
            res.end();
        });
    }
});

server.get("/programs/:name", function (req, res, next) {
    var name = req.params.name;

    if (req.headers["accept"] !== "application/lua") {
        reportError("'GET /programs/" + name + "' requires 'Content-Type: application/lua'.");
    }

    if (programs[name]) {
        res.writeHead(200, {
            "Content-Type": "application/lua",
            "Content-Length": programs[name].length,
            "Collection-Item": name,
        });
        res.write(programs[name]);
        res.end();

    } else {
        res.writeHead(404);
        res.end();
    }
});

server.del("/programs/:name", function (req, res, next) {
    var name = req.params.name;

    delete programs[name];
    res.writeHead(204, {
        "Collection-Item": name,
    });
    res.end();
});

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


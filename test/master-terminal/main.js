var restify = require("restify");
var db = require("./database.js");

// Creates a new Restify server.
var server = restify.createServer();

// This adds query information to 'req' variable in resource handles.
server.use(restify.queryParser());

server.get("/sensors", function (req, res, next) {
    if (req.headers["accept"] !== "application/json") {
        reportError("'GET /sensors' requires 'Accept: application/json'.");
    }

    var sensorResult = [];

    if (req.query.room) {
        if (req.query.room === "null") {
            sensorResult = db.sensors.filter(function (s) {
                return !s.room;
            });

        } else {
            sensorResult = db.sensors.filter(function (s) {
                return s.room === req.query.room;
            });
        }
    } else {
        sensorResult = db.sensors;
    }
    var sensorNames = sensorResult.map(function (s) {
        return s.id;
    });

    var sensorBuffer = new Buffer(JSON.stringify(sensorResult));
    res.writeHead(200, {
        "Content-Type": "application/json",
        "Content-Length": sensorBuffer.length,
        "Collection-items": sensorNames.join(","),
    });
    res.write(sensorBuffer);
    res.end();

    next();
});

server.put("/sensors/:id/room", function (req, res, next) {
    var id = req.params.id;

    if (req.headers["content-type"] !== "text/plain") {
        reportError("'PUT /sensors/" + id + "/room' requires 'Content-Type: text/plain'.");
    }

    var target = null;
    db.sensors.forEach(function (s) {
        if (s.id === id) {
            target = s;
        }
    });

    if (target === null) {
        res.writeHead(404);
        res.end();

    } else {
        target.room = null;
        req.on("data", function (data) {
            target.room = data.toString();
            res.writeHead(204);
            res.end();
        });
    }

    next();
});

server.head("/programs", function (req, res, next) {
    if (req.headers["accept"] !== "application/lua") {
        reportError("'HEAD /programs' requires 'Accept: application/lua'.");
    }
    res.writeHead(200, {
        "Content-Type": "application/lua",
        "Content-Length": 0,
        "Collection-Items": Object.keys(db.programs).join(","),
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

    } else if (db.programs[name]) {
        res.writeHead(403, {
            "Content-Type": "text/plain",
        });
        res.write("A program with that name already exists.");
        res.end();

    } else {
        req.on("data", function (data) {
            db.programs[name] = data.toString();
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

    if (db.programs[name]) {
        res.writeHead(200, {
            "Content-Type": "application/lua",
            "Content-Length": db.programs[name].length,
            "Collection-Item": name,
        });
        res.write(db.programs[name]);
        res.end();

    } else {
        res.writeHead(404);
        res.end();
    }
});

server.del("/programs/:name", function (req, res, next) {
    var name = req.params.name;

    delete db.programs[name];
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
}, 50000);


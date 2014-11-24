var db = require("../database.js");

module.exports = {
    register: function (server, reportError) {

        server.get("/actuators", function (req, res, next) {
            if (req.headers["accept"] !== "application/json") {
                reportError("'GET /actuators' requires 'Accept: application/json'.");
            }
        
            var actuatorResult = [];
        
            if (req.query.room) {
                if (req.query.room === "null") {
                    actuatorResult = db.actuators.filter(function (a) {
                        return !a.room;
                    });
        
                } else {
                    actuatorResult = db.actuators.filter(function (a) {
                        return a.room === req.query.room;
                    });
                }
            } else {
                actuatorResult = db.actuators;
            }
            var actuatorNames = actuatorResult.map(function (a) {
                return a.id;
            });
        
            var actuatorBuffer = new Buffer(JSON.stringify(actuatorResult));
            res.writeHead(200, {
                "Content-Type": "application/json",
                "Content-Length": actuatorBuffer.length,
                "Collection-items": actuatorNames.join(","),
            });
            res.write(actuatorBuffer);
            res.end();
        
            next();
        });
        
        server.put("/actuators/:id/room", function (req, res, next) {
            var id = req.params.id;
        
            if (req.headers["content-type"] !== "text/plain") {
                reportError("'PUT /actuators/" + id + "/room' requires 'Content-Type: text/plain'.");
            }
        
            var target = null;
            db.actuators.forEach(function (a) {
                if (a.id === id) {
                    target = a;
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

    }
};


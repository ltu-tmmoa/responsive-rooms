var db = require("../database.js");

module.exports = {
    register: function (server) {

        server.get("/actuators", function (req, res, next) {
            if (req.headers["accept"] !== "application/json") {
                console.log("'GET /actuators' requires 'Accept: application/json'.");
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
                console.log("'PUT /actuators/" + id + "/room' requires 'Content-Type: text/plain'.");
            }
            if (typeof req.headers["content-length"] === "undefined") {
                console.log("'PUT /actuators/" + id + "/room' requires 'Content-Length'.");
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
                if ((req.headers["content-length"] | 0) > 0) {
                    req.on("data", function (data) {
                        target.room = data.toString();
                        res.writeHead(204);
                        res.end();
                    });  
                } else {
                    target.room = null;
                    res.writeHead(204);
                    res.end();
                }
            }
        
            next();
        });

    }
};


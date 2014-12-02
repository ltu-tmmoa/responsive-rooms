var db = require("../database.js");

module.exports = {
    register: function (server) {

        server.get("/sensors", function (req, res, next) {
            if (req.headers["accept"] !== "application/json") {
                console.log("'GET /sensors' requires 'Accept: application/json'.");
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
                console.log("'PUT /sensors/" + id + "/room' requires 'Content-Type: text/plain'.");
            }
            if (typeof req.headers["content-length"] === "undefined") {
                console.log("'PUT /sensors/" + id + "/room' requires 'Content-Length'.");
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


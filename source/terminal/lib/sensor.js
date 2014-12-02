(function () {
  "use strict";

  var Promise = require("promise");
  var http = require("http");

  var actions = {
    /**
     * Lists sensors, potentially filtering by status.
     */
    list: function (host, pathRoot, filter) {
      return new Promise(function (fulfill, reject) {
        var query = "";
        if (filter) {
          if (filter === "unassigned") {
            query = "?room=null";
          } else {
            query = "?room=" + filter;
          }
        }
        http.request({
          host: host,
          path: pathRoot + query,
          method: "GET",
          headers: {
            "accept": "application/json",
          },
          port: 14003,
        }, function (res) {
          if (res.statusCode === 200) {
            res.on("data", function (data) {
              fulfill(JSON.parse(data));
            });

          } else {
            reject("Unable to list sensors.");
          }
        })
        .on("error", reject)
        .end();
      });
    },

    /**
     * Assigns sensor with given ID a room.
     */
    assign: function (host, pathRoot, id, room) {
      return new Promise(function (fulfill, reject) {
        if (!id) {
          reject("Please provide a sensor ID.");
          return;
        }
        if (!room) {
          reject("Please provide a room to assign to.");
          return;
        }
        assign(host, pathRoot, id, room)
          .then(function (text) {
            if (!text) {
              text = "Assigned '" + id + "' to room '" + room + "'.";
            }
            fulfill(text);
          }, function (error) {
            if (!error) {
              error = "Failed to assign '" + id + "' to room '" + room + "'.";
            }
            reject(error);
          });
      });
    },

    /**
     * Unassigns identified sensor from given room.
     */
    unassign: function (host, pathRoot, id) {
      return new Promise(function (fulfill, reject) {
        if (!id) {
          reject("Please provide a sensor ID.");
          return;
        }
        assign(host, pathRoot, id, room)
          .then(function (text) {
            if (!text) {
              text = "Unassigned '" + id + "'.";
            }
            fulfill(text);
          }, function (error) {
            if (!error) {
              error = "Failed to unassign '" + id + "'.";
            }
            reject(error);
          });
      });
    },
  };

  function assign(host, pathRoot, id, room) {
    return new Promise(function (fulfill, reject) {
      if (typeof room !== "string") {
        room = "";
      }
      http.request({
        host: host,
        path: pathRoot + "/" + id + "/room",
        method: "PUT",
        headers: {
          "content-type": "text/plain",
          "content-length": room.length,
        },
        port: 14003,
      }, function (res) {
        if (res.statusCode === 204) {
          fulfill();

        } else if (res.statusCode === 404) {
          reject("Noone with ID '" + id + "'.");

        } else {
          reject();
        }
      })
      .on("error", reject)
      .end(room);
    });
  }

  exports.onAction = function (host, action, param1, param2) {
    var f = actions[action];
    if (f) {
      return f(host, "/sensors", param1, param2);
    }
    throw new Error("No such sensor action.");
  };

  exports.getSubActions = function () {
    return [
      "list",
      "list unassigned",
      "assign",
      "unassign",
    ];
  };

}());

(function () {
  "use strict";

  var Promise = require("promise");
  var http = require("http");

  /**
   * Handles some terminal action.
   */
  exports.onAction = function (host, action, param1, param2) {
    var f = actions[action];
    if (f) {
      return f(host, param1, param2);
    }
    throw new Error("No such sensor action.");
  };

  var actions = {
    /**
     * Lists sensors, potentially filtering by status.
     */
    list: function (host, filter) {
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
          path: "/sensors" + query,
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
    assign: function (host, id, room) {
      return new Promise(function (fulfill, reject) {
        if (!id) {
          reject("Please provide a sensor ID.");
          return;
        }
        if (!room) {
          reject("Please provide a room to assign sensor to.");
          return;
        }
        assign(host, id)
          .then(function (text) {
            if (!text) {
              text = "Assigned sensor '" + id + "' to room '" + room + "'.";
            }
            fulfill(text);
          }, function (error) {
            if (!error) {
              error = "Failed to assign sensor '" + id + "' to room '" + room + "'.";
            }
            reject(error);
          });
      });
    },

    /**
     * Unassigns identified sensor from given room.
     */
    unassign: function (host, id) {
      return new Promise(function (fulfill, reject) {
        if (!id) {
          reject("Please provide a sensor ID.");
          return;
        }
        assign(host, id, room)
          .then(function (text) {
            if (!text) {
              text = "Unassigned sensor '" + id + "'.";
            }
            fulfill(text);
          }, function (error) {
            if (!error) {
              error = "Failed to unassign sensor '" + id + "'.";
            }
            reject(error);
          });
      });
    },
  };

  function assign(host, id, room) {
    return new Promise(function (fulfill, reject) {
      if (typeof room !== "string") {
        room = "";
      }
      http.request({
        host: host,
        path: "/sensors/" + id + "/room",
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

  /**
   * Provides a list of subactions for the command completer.
   */
  exports.getSubActions = function () {
    return [
      "list",
      "list unassigned",
      "assign",
      "unassign",
    ];
  };

}());

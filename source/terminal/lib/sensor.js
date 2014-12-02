(function () {
  "use strict";

  var Promise = require("promise");
  var http = require("http");

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
        
      });
    },

    /**
     * Unassigns identified sensor from given room.
     */
    unassign: function (host, id) {
      return new Promise(function (fulfill, reject) {
        
      });
    },
  };

  exports.onAction = function (host, action, param1, param2) {
    var f = actions[action];
    if (f) {
      return f(host, param1, param2);
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

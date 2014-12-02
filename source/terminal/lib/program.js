(function () {
  "use strict";

  var http = require("http");
  var Promise = require("promise");

  var actions = {
    /**
     * Adds named program to master at host.
     */
    add: function (host, programName) {
      return new Promise(function (fulfill, reject) {
        fulfill();
      });
    },

    /**
     * Retrieves filtered list of programs from master, which is the displayed.
     */
    list: function (host, filter) {
      return new Promise(function (fulfill, reject) {
        http.request({
          host: host,
          path: "/programs",
          method: "HEAD",
          headers: {
            "accept": "application/lua",
          },
          port: 14003,
        }, function (res) {
          if (res.statusCode === 200) {
            fulfill(res.headers["collection-items"].split(",").join("\r\n"));

          } else {
            reject("Failed to retrieve program list from host '" + host + "'.");
          }
        })
        .on("error", reject).end();
      });
    },

    /**
     * Removed named program from master at host.
     */
    remove: function (host, programName) {
      return new Promise(function (fulfill, reject) {
        if (!programName) {
          reject("Please state the name of a program to remove.");
          return;
        }
        http.request({
          host: host,
          path: "/programs/" + programName,
          method: "DELETE",
          port: 14003,
        }, function (res) {
          if (res.statusCode === 204) {
            fulfill("Removed '" + res.headers["collection-item"] + "'.");
          }
          reject("Failed to remove program '" + programName + "'.");
        })
        .on("error", reject).end();
      });
    },
  };

  exports.onAction = function (host, action, param) {
    var f = actions[action];
    if (f) {
      return f(host, param);
    } 
    throw new Error("No such program action.");
  };

  exports.getSubActions = function () {
    return Object.keys(actions);
  };

}());


(function () {
  "use strict";

  var fs = require("fs");
  var http = require("http");
  var Promise = require("promise");

  var actions = {
    /**
     * Adds named program to master at host.
     */
    add: function (host, programPath) {
      return new Promise(function (fulfill, reject) {
        fs.readFile(programPath, function (error, data) {
          if (error) {
            reject("Failed to read file '" + programPath + "'.");
          } else {
            http.request({
              host: host,
              path: "/programs",
              method: "POST",
              headers: {
                "accept": "text/plain",
                "content-type": "application/lua",
                "collection-item": programPath,
              },
              port: 14003,
            }, function (res) {
              res.on("data", function (data) {
                if (res.statusCode === 201) {
                  fulfill("Added program '" + data.toString() + "'.");
                } else {
                  reject(data.toString());
                }
              });
            })
            .on("error", reject)
            .end(data);
          }
        });
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
        .on("error", reject)
        .end();
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
        .on("error", reject)
        .end();
      });
    },

    view: function (host, programName) {
      return new Promise(function (fulfill, reject) {
        if (!programName) {
          reject("Please state the name of a program to view.");
          return;
        }
        http.request({
          host: host,
          path: "/programs/" + programName,
          method: "GET",
          port: 14003,
        }, function (res) {
          if (res.statusCode === 200) {
            res.on("data", function (data) {
              fulfill(data.toString());
            });
          } else if (res.statusCode === 404) {
            reject("Program '" + programName + "' not found.");

          } else {
            reject("Failed to view program '" + programName + "'.");
          }
        })
        .on("error", reject)
        .end();
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


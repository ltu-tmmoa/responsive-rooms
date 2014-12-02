(function () {
  "use strict";

  var http = require("http");

  var actions = {
    /**
     * Adds named program to master at host.
     */
    add: function (host, programName) {

    },

    /**
     * Retrieves filtered list of programs from master, which is the displayed.
     */
    list: function (host, filter) {
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
          res.headers["collection-items"].split(",").forEach(function (item) {
            console.log("  " + item);
          });

        } else {
          console.log("error");
        }
      })
      .on("error", function (error) {
        console.log(error);
      }).end();
    },

    /**
     * Removed named program from master at host.
     */
    remove: function (host, programName) {

    },
  };

  exports.onAction = function (host, action, param) {
    var f = actions[action];
    if (f) {
      f(host, param);

    } else {
      throw new Error("No such program action.");
    }
  };

  exports.getSubActions = function () {
    return Object.keys(actions);
  };

}());


(function () {
  "use strict";

  var Promise = require("promise");

  exports.onAction = function (host, action, param1, param2) {
    return new Promise(function (fulfill, reject) {
      fulfill();
    });
  };

  exports.getSubActions = function () {
    return [
      "list",
      "list unassigned",
      "list unresponsive",
      "assign",
      "unassign",
    ];
  };

}());

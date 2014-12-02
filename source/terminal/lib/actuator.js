(function () {
  "use strict";

  exports.onAction = function (host, action, param1, param2) {
    console.log(arguments);
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


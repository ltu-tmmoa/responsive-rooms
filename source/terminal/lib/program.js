(function () {
  "use strict";

  exports.onAction = function (host, action, param) {
    console.log(arguments);
  };

  exports.getSubActions = function () {
    return [
      "add",
      "list",
      "remove",
    ];
  };

}());


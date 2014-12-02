(function () {
  "use strict";

  var readline = require("readline");
  var colors = require("colors/safe");

  /**
   * Creates a new terminal handler.
   *
   * The terminal handler keeps track of a terminal prompt, and mapping its
   * input to registered action handlers.
   *
   * The given default arguments, if any, are always passed to registered action
   * handlers.
   */
  function Terminal(handlerDefaultArgs) {
    if (!Array.isArray(handlerDefaultArgs)) {
      handlerDefaultArgs = [handlerDefaultArgs];
    }
    this.handlerDefaultArgs = handlerDefaultArgs;
    this.actions = {};

    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      completer: completer,
    });
    this.rl.setPrompt("> ", 2);
    this.rl.pause();

    var that = this;
    function completer(line) {
      var completions = Object.keys(that.actions);
      var lineWords = line.split(" ").length;

      var hits = completions.filter(function (completion) {
        var completionWords = completion.split(" ").length;
        return completion.indexOf(line) === 0 &&
          lineWords === completionWords;
      });
      return [hits, line];
    }
  }

  /**
   * Registers given action handler, potentially replacing an existing handler
   * with the same action name.
   *
   * The handler will be called with the terminal handler default arguments
   * followed by the parameters following the action typed by the user.
   *
   * Returns a reference to the current terminal to allow method chaining.
   */
  Terminal.prototype.register = function (action, handler) {
    this.actions[action] = handler;

    var that = this;
    if (typeof handler === "object" && handler.getSubActions) {
      handler.getSubActions().forEach(function (subAction) {
        that.actions[action + " " + subAction] = handler;
      });
    }
    return this;
  };

  /**
   * Registers close event handler.
   *
   * Returns a reference to the current terminal to allow method chaining.
   */
  Terminal.prototype.onClose = function (callback) {
    this.rl.on("close", callback);
    return this;
  };

  /**
   * Starts execution of terminal.
   */
  Terminal.prototype.exec = function (callback) {
    var that = this;

    resume();

    this.rl.on("line", function (line) {
      var args = line.split(" ");
      var action = that.actions[args[0]];
      var parameters = that.handlerDefaultArgs.concat(args.slice(1));

      that.rl.pause();
      try {
        var promise;
        if (typeof action === "object") {
          promise = action.onAction.apply(action, parameters);

        } else if (typeof action === "function") {
          promise = action.apply(null, parameters);

        } else {
          throw new Error("Unsupported action '" + args[0] + "'.");
        }
        promise.then(resume, function (error) {
          if (!(error instanceof Error)) {
            error = new Error(error);
          }
          resume(error);
        });

      } catch (error) {
        resume(error);
      }
    });

    function resume(message) {
      if (message) {
        if (message instanceof Error) {
          message = colors.red("! " + message.message);
        }
        console.log(message);
      }
      that.rl.prompt();
      that.rl.resume();
    }
  };

  /**
   * Closes terminal.
   */
  Terminal.prototype.close = function () {
    this.rl.close();
  };

  module.exports = Terminal;
}());

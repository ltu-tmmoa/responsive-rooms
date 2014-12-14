var dgram = require("dgram");
var net = require("net");
var hue = require("./hue");
var Promises = require("promise");

var jf = require("jsonfile");
var util = require("util");
var file = "./actuatorContext.json";

var AM = {
  "message": "AM",
  "type": "light",
  "properties": {
    "transition": "int",
    "alert": "boolean",
    "brightness": "int",
    "color": {
      "red": "int",
      "green": "int",
      "blue": "int",
    },
  },
  "context": null
};
var AR = {
  "message": "AR",
  "type": "light",
  "properties": {
    "transition": "0",
    "alert": "false",
    "brightness": "0",
    "color": {
      "red": "0",
      "green": "0",
      "blue": "0",
    },
  },
  "context": null
};
var ER = {
  "message": "ER",
  "error": "you suck :)"
};
var CU;

readFromFile();
hue.changeLightStatus(AR);
setTimeout(function() {
  start();
}, 100);

function start() {
  console.log("Start is invoked");
  bind()
    .then(register)
    .then(runTime)
    .then(report)
    .catch(displayError)
    .done();
}

function bind() {
  return new Promises(function(fulfill, reject) {
    var server = dgram.createSocket("udp4");
    server.on("listening", function() {
      var address = server.address();
      console.log("server listening " +
        address.address + ":" + address.port);
    });
    server.on("message", function(msg, rinfo) {
      console.log("server got: " + msg + " from " +
        rinfo.address + ":" + rinfo.port);

      if (validJSON(msg)) {
        var temp = JSON.parse(msg);
        if (temp.message == "MD") {
          server.close();
          console.log("terminate UDP");
          fulfill(rinfo);
        }
      }
    });
    server.bind(14000);
    server.on("error", function(error) {
      server.close();
      setTimeout(function() {
        start();
      }, 1000);
      reject(error);
    });
  });
}

function register(rinfo) {
  return new Promises(function(fulfill, reject) {

    var socket = new net.Socket();
    socket.on("error", function(error) {
      console.log("Socket error " + error);
    });
    socket.on("close", function() {
      console.log("Socket closed");
      clearInterval(xz);
      socket.destroy();
      setTimeout(function() {
        start();
      }, 2000);
    });
    socket.connect(14002, rinfo.address, function() {
      console.log("connected using Tcp");
      socket.write(JSON.stringify(AM), function() {
        console.log("AM is been sent");
        fulfill(socket);
      });
    });
  });
}

function runTime(socket) {
    return new Promises(function(fulfill, reject) {
      console.log("runTime is invoked ");
      socket.on('data', function(data) {
        if (validJSON(data)) {
          msg = JSON.parse(data);
          switch (msg.message) {
            case "CU":
              console.log("received CU");
              writeToFile(msg);
              break;
            case "AU":
              console.log("received AU");
              AR = msg;
              AR.message = "AR";
              AR.context = CU;
              hue.changeLightStatus(msg);
              break;
            default:
              socket.write(JSON.stringify(ER));
          }
        }
      });
      fulfill(socket);
    });
  }
  // xy to clearInterval using socket.on("close", function(){})
var xz;

function report(socket) {
  return new Promises(function(fulfill, reject) {
    xz = setInterval(function() {
      hue.getLightStatus(function(status) {
        //AR.properties.color.red = status.r;
        //AR.properties.color.green = status.g;
        //AR.properties.color.blue = status.b;
        socket.write(JSON.stringify(AR), function() {
          console.log("status is sent");
        });
      });
    }, 5000);
    fulfill(socket);
  });
}

function writeToFile(msg) {
  delete msg.message;
  CU = msg;
  AR.context = CU;
  AM.context = CU;
  jf.writeFile(file, CU, function(error) {
    if (error) {
      console.log(error);
    }
  });
}

function readFromFile() {
  jf.readFile(file, function(error, obj) {
    if (error) {
      console.log(error);
    } else {
      CU = obj;
      AR.context = CU;
      AM.context = CU;
    }
  });
}

function validJSON(msg) {
  try {
    var message = JSON.parse(msg);
    return true;
  } catch (error) {
    console.log("Non JSON message");
    return false;
  }
}

function displayError(error) {
  console.log(error);
}

// Catch all errors
//process.on('uncaughtException', function(err) {
//  console.log('Caught exception: ' + err);
//});
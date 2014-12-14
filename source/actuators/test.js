var dgram = require('dgram');
var client = dgram.createSocket('udp4');
var Promises = require("promise");
var port = 14000;
var host = '127.0.0.1';
var net = require('net');
var MD = {
  "message": "MD"
};
var md = new Buffer(JSON.stringify(MD));
var AU = {
  "message": "AU",
  "type": "light",
  "properties": {
    "transition": "5",
    "alert": "false",
    "brightness": "100",
    "color": {
      "red": "200",
      "green": "100",
      "blue": "100",
    },
  },
};
var CU = {
  "message": "CU",
  "facility": "A",
  "room": "1202",
  "location": {
    "x": 4.5,
    "y": 1.9,
    "z": 6.2
  }
};
broadcastMd()
  .then(createTcpServer)
  .then(handelSocket)
  .then(timeOut)
  .then(sendCu)
  .then(timeOut)
  .then(sendAu)
  .then(finPacket)
  .catch(displayError)
  .done();

function broadcastMd() {
    return new Promises(function(fulfill, reject) {
      console.log("broadcastMd is invoked");
      x = setInterval(function() {
        client.send(md, 0, md.length, port, host, function(error) {
          console.log("MD is sent");
          if (error) {
            console.log(error);
            clearInterval(x);
            reject(error);
          } else {
            fulfill();
          }
        });
      }, 2000);
    });
  }
  //call handelSocket after the first run
var n = 0;

function createTcpServer() {
  return new Promises(function(fulfill, reject) {
    console.log("createTcpServer is invoked");
    var server = net.createServer(function(socket) {
      console.log("Create a Socket");
      fulfill(socket);
      //call handelSocket after the first run
      if (n !== 0) {
        handelSocket(socket);
      }
      n = 1;
    });
    server.listen(14002, function() {
      console.log("Tcp server on port : 14002");
    });
    server.on("connect", function() {
      console.log("An actuator is connected using Tcp");
    });
  });
}

function handelSocket(socket) {
  return new Promises(function(fulfill, reject) {
    console.log("handelTcp is invoked");
    //socket.setTimeout(5000);
    socket.on("error", function(error) {
      console.log("Socket error" + error);
      socket.destroy();
    });
    socket.on("close", function() {
      console.log("Socket closed");
    });
    socket.on('data', function(data) {
      if (validJSON(data)) {
        var msg = JSON.parse(data);
        switch (msg.message) {
          case "AM":
            console.log("Got an AM message");
            console.log(JSON.stringify(msg, null, 2));
            break;
          case "AR":
            console.log("Got an AR message");
            console.log(JSON.stringify(msg, null, 2));
            break;
          case "ER":
            console.log("Got an ER message");
            console.log(JSON.stringify(msg, null, 2));
            break;
          default:
            console.log("random msg \n" + JSON.stringify(msg, null, 2));
        }
      }
    });
    fulfill(socket);
  });
}

function timeOut(socket) {
  return new Promises(function(fulfill, reject) {
    setTimeout(function() {
      fulfill(socket);
    }, 2000);
  });
}

function finPacket(socket) {
  return new Promises(function(fulfill, reject) {
    setTimeout(function() {
      console.log("Sent a Fin packet");
      socket.end();
      fulfill(socket);
    }, 10000);
  });
}

function sendAu(socket) {
  return new Promises(function(fulfill, reject) {
    socket.write(JSON.stringify(AU));
    console.log("Sent AU message");
    fulfill(socket);
  });
}

function sendCu(socket) {
  return new Promises(function(fulfill, reject) {
    socket.write(JSON.stringify(CU));
    console.log("Sent CU message");
    fulfill(socket);
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
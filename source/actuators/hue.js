var hue = require("node-hue-api");
var userName = "150369a32f054e0f430369bf453d87";
var ipAddress = '192.168.1.2';
var api = new hue.HueApi(ipAddress, userName);

function displayError(error) {
  console.log("Can't connect to the bridge");
  console.log(error);
}
hue.searchForBridges(5000)
  .then(displayResult)
  .catch(displayError)
  .done();

function displayResult(result) {
  console.log(JSON.stringify(result, null, "\t"));
}

module.exports = {
  getLightStatus: function(callback) {
    api.lightStatus(3)
      //.then(lambstate)
      .then(callback)
      .catch(displayError)
      .done();
  },
  changeLightStatus: function(lightstatus) {
    var api = new hue.HueApi(ipAddress, userName);
    /* lightState object
    .rgb(red, green, blue)
    .brightness(percent)
    .alert() flash the light once,passing isLong flash it
    10 times.
    .transition(seconds) this can be used with another
    setting to create a transition effect (like change
    brightness over 10 seconds)
    */
    var transition = parseInt(lightstatus.properties.transition);
    var alert = lightstatus.properties.alert; //bolean
    var brightness = parseInt(lightstatus.properties.brightness);
    var red = parseInt(lightstatus.properties.color.red);
    var green = parseInt(lightstatus.properties.color.green);
    var blue = parseInt(lightstatus.properties.color.blue);
    if (alert == "true") {
      alert = "isLong";
    } else {
      alert = null;
    }
    var state;
    if (brightness === 0) {
      state = hue.lightState.create()
        .off();
    } else {
      state = hue.lightState.create()
        .on()
        .rgb(red, green, blue)
        .transition(transition)
        .alert(alert)
        .brightness(brightness);
    }


    api.setLightState(3, state)
      .then(function() {
        console.log("Light status been changed");
      })
      .catch(displayError)
      .done();
  }
};

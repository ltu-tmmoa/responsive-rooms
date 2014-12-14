var hue = require("node-hue-api");
var userName = "";
var ipAddress = "";
var api = new hue.HueApi(ipAddress, userName);

function displayError(error) {
  console.log("Can't connect to the bridge");
}

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
    var alert = lightstatus.properties.alert;
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
/* xy to rgb but it's not working well

function lambstate(statusXy) {
var x = statusXy.state.xy[0];
var y = statusXy.state.xy[1];
var bri = statusXy.state.bri;
return xyBriToRgb(x, y, bri);

}

function xyBriToRgb(x, y, bri) {
z = 1.0 - x - y;
Y = bri / 255.0;
X = (Y / y) * x;
Z = (Y / y) * z;
r = X * 1.612 - Y * 0.203 - Z * 0.302;
g = -X * 0.509 + Y * 1.412 + Z * 0.066;
b = X * 0.026 - Y * 0.072 + Z * 0.962;
r = r <= 0.0031308 ? 12.92 * r : (1.0 + 0.055) * Math.pow(r, (1.0 / 2.4)) - 0.055;
g = g <= 0.0031308 ? 12.92 * g : (1.0 + 0.055) * Math.pow(g, (1.0 / 2.4)) - 0.055;
b = b <= 0.0031308 ? 12.92 * b : (1.0 + 0.055) * Math.pow(b, (1.0 / 2.4)) - 0.055;
maxValue = Math.max(r, g, b);
r /= maxValue;
g /= maxValue;
b /= maxValue;
r = r * 255;
if (r < 0) {
r = 255;
}
g = g * 255;
if (g < 0) {
g = 255;
}
b = b * 255;
if (b < 0) {
b = 255;
}
return {
r: r,
g: g,
b: b
};
}
*/
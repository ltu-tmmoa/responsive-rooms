// A naive non-persistent collection of data available through the mock-up
// service.
module.exports = {
    sensors: [
        {
            id: "0", room: "A1", type: "thermometer",
            properties: {
                celcius: "number",
                fahrenheit: "number",
            },
        },
        {
            id: "1", room: null, type: "thermometer",
            properties: {
                celcius: "number",
                fahrenheit: "number",
            },
        }
    ],
    actuators: [
        {
            id: "A", room: "A1", type: "alarm",
            properties: {
                fired: "boolean",
            },
        },
        {
            id: "B", room: null, type: "alarm",
            properties: {
                fired: "boolean",
            },
        },
    ],
    programs: {
        "temp_alarm.lua": "--[[Some lua code.]]--",
        "temp_monitor.lua": "--[[Some more lua code.]]--",
    },
};

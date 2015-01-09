#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>         

#define TRIG_PIN 6       // Transmit signal pin of an ultrasound distance.
#define ECHO_PIN 7       // The received echo pin.
#define CONTEXT_SIZE 512 // Size of context (CU) string.
#define REPORT_SIZE 64   // Size of a report (SR) string.

unsigned int LOCAL_PORT = 14000;
byte LOCAL_MAC[] = {0x90, 0xA2, 0xDA, 0x0F, 0x97, 0x98 };

EthernetUDP udp;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];

EthernetClient tcp;
IPAddress remoteip(0,0,0,0);
char context[CONTEXT_SIZE];
char report[REPORT_SIZE];

void setup() { 
  Serial.begin(9600);
  while (!Serial)
    delay(1000);

  Serial.println("Waiting for an IP ...");
  while (Ethernet.begin(LOCAL_MAC) == 0)
    delay(1000);

  Serial.println("Obtained an IP Address:");
  Serial.println(Ethernet.localIP());

  context[0] = '\0';

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT); 
}

boolean isConnected = false;

void loop() {
  if (!isConnected) {
    rr_init();
  } else {
    rr_run();
  }
  rr_wait();
}

void rr_init(){
  if (rr_bind()) {
    if (rr_listen()) {
      rr_unbind();
      if (rr_connect()) {
        if (rr_register()) {
          rr_send_context();
          isConnected = true;
          return;
        }
      }
    } else {
      rr_unbind();
    }
  }
}

boolean rr_bind() { 
  Serial.println("Binding UDP port ...");
  int s = udp.begin(LOCAL_PORT);
  delay(1000);
  return s == 1;
}

boolean rr_listen() {
  int packetSize =udp.parsePacket(); //check the presence of packets
    if (packetSize)
    { udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE); // read existing udp packages content
      Serial.println("Contents:");
      Serial.println(packetBuffer);
      remoteip = udp.remoteIP();
      Serial.println(remoteip);
      return true;
    }
     else {
    Serial.println("failed to listen");
    return false;
  }
    }

void rr_unbind() {
   udp.stop();
   delay(1000);
   Serial.println("unbind");
}

boolean rr_connect() {
  int s = tcp.connect(remoteip, 14001);
  delay(1000);
  if (s == 1){
   Serial.println("TCP connection");
   return true;
 } else {
    Serial.print("connection failed with status ");
    Serial.println(s);
    return false;
  }
}

boolean rr_register() {
  Serial.println("registering...");
  if (tcp.connected()) {
    tcp.println("{\"message\":\"SM\",\"type\":\"\proximity\",\"properties\":{\"centimeters\":\"number\"}}");
    Serial.println("registered");
    return true;
  } else {
    Serial.println("failed to register");
    return false;
  }
}

void rr_send_context() {
  if (context[0] != '\0') {
    tcp.println(context);
    Serial.println("Sent context.");
  }
}

void rr_run() {
  /*if (!rr_receive()) {
    isConnected = false;
    return;
  }*/
  if (!rr_report()) {
    isConnected = false;
  }
}

boolean rr_receive() {
  if (!tcp.connected()) {
    tcp.flush();
    tcp.stop();
    return false;
  }
  if (tcp.available()) {
    int i = 0;
    int c;
    while ((c = tcp.read()) != -1 && i < CONTEXT_SIZE) {
      context[i] = c;
      i += 1;
    }
    context[i] = '\0';
    Serial.println("Received context:");
    Serial.println(context);
  }
  return true;
}

boolean rr_report() {
  if (!tcp.connected()) {
    tcp.flush();
    tcp.stop();
    return false;
  }
  snprintf(report, REPORT_SIZE, "{\"message\":\"SR\",\"properties\":{\"centimeters\":%d}}", readSensorDistance());
  tcp.println(report);
  
  Serial.println("Sent report:");
  Serial.println(report);

  delay(1000);

  return true;
}

int readSensorDistance() {
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(1000);
  digitalWrite(TRIG_PIN, LOW);
  int duration = pulseIn(ECHO_PIN, HIGH) / 2;
  return duration / 29.1;
}

void rr_wait() {
  delay(1000);
}

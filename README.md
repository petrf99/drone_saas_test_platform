# 🛰️ Genesis Remote Flights PLatform (GRFP)

## 🎯 Purpose
This platform enables remote piloting of real drones over the internet, including FPV, for use cases such as certification exams, training, and live operations. A remote operator (e.g., in the US) can control a drone located in another country (e.g., Paraguay) via a secure, low-latency pipeline.

---

## 🧱 Components

1. **Client App (Python)**
   - Local application running on the operator's machine.
   - Supports various controllers: keyboard, gamepad, RC transmitter.
   - Sends RC frames via VPN to the Ground Station (GCS).
   - Receives live video and telemetry from the drone.
   - Built with `pygame`.

2. **Dispatcher (RFD)**
   - Central mission coordinator and state manager.
   - Processes mission requests, payments, and authorizations.
   - Issues session tokens and coordinates VPN sessions.

3. **Ground Control Station (GCS)**
   - Deployed on-site with Starlink uplink.
   - A laptop or Raspberry Pi connected to a radiomodem.
   - Receives RC input via VPN, relays commands to drone via MAVLink.
   - Sends telemetry and video stream back to client via VPN.

4. **Drone**
   - Equipped with PX4 or ArduPilot firmware.
   - Connected to a radiomodem for ground communication.
   - Streams telemetry and video via MAVLink.

5. **Client Web Interface**
   - Web portal where users request missions, choose drones and controllers, and make payments.
   - Displays mission tokens and statuses.

6. **Engineering Team**
   - On-site personnel responsible for setting up and launching the drone and GCS.
   - Confirms readiness and starts the mission session.

---

## 🔁 Session Workflow

1. Client creates a mission via the web interface (specifying drone, time, location, control type).
2. Dispatcher assigns it to an engineering team who reviews and approves the mission.
3. After client payment, mission status is updated to “in progress.”
4. Engineering team sets up GCS and the drone on location.
5. Dispatcher marks mission as ready and sends the access token to the client.
6. Client launches the Python application and inputs the token.
7. Dispatcher enables a Tailscale VPN session linking Client ↔ GCS.
8. Client streams RC frames to GCS via VPN (JSON or MAVLink).
9. GCS relays commands to the drone via the radiomodem.
10. Telemetry and live video are streamed back to the client through the same VPN.
11. Client sees video and controls the drone from a single interface.

---

## 🔐 Highlights

- **Tailscale VPN** for seamless NAT traversal and secure connection.
- **Ultra-low latency**: direct UDP pipelines (no WebRTC).
- GCS acts as a **local MAVLink proxy** between client and drone.
- Video is streamed via **MJPEG or H.264 over UDP**.
- Architecture supports further extensions: simulators, autopilot protocols, or multi-client scenarios.

---

This README serves as a technical overview for developers, investors, or collaborators. For any assistance, contact the core architecture team.
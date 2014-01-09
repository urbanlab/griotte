************
Architecture
************

Griotte uses Tornado as a web/websockets server. All clients (server side
clients like analog sensors handlers, web interface, ...) communicate using
websockets in a pub/sub fashion, making it easy to add more clients, more server
side handlers, ...

For instance, if one client (e.g. a scenario running) is interested in a sensor
value, it just needs to subscribe to this sensor's channel, and will get
messages when values are available.

Using websockets also provides a real time communication
channel when multiple clients interact with the Griotte system.

Server side clients run in their own process, so they can easily be started,
stopped, restarted without impacting the whole system.



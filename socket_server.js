let HOST = '127.0.0.1'
let PORT = 8000;
let dgram = require('dgram');
let server = dgram.createSocket('udp4');

server.on('message', function(message, remote) {
    console.log(''+message);
})
server.bind(PORT,HOST);
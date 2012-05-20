var net = require('net');

var server = net.createServer(function(socket) {
    socket.on('data', function(data) {

        var options = {
          host: 'isithackday.com',
          port: 80,
          path: '/arrpi.php?text='+data
        };

        http.get(options, function(res) {
          socket.write(res);
        }).on('error', function(e) {
          console.log("Got error: " + e.message);
        });
    });
});

server.listen(8000);

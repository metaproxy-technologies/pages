var app  = require('express')();
var http = require('http').Server(app);
var io   = require('socket.io')(http);
var SerialPort  = require('serialport');
var sp = new SerialPort('/dev/ttyACM0', {
  baudRate: 9600,
  dataBits: 8,
  parity: 'none',
  stopBits: 1,
  flowControl: false
});

var interval = 100; //ms
var last = Date.now();

function buildByteGP(gp){
  /*
  [bit assignment]
   FORWARD  -> 1000 0000 -> 0x80
   BACKWARD -> 0100 0000 -> 0x40
   LEFT     -> 0010 0000 -> 0x20
   RIGHT    -> 0001 0000 -> 0x10
   STOP     -> 0000 0001 -> 0x01

  [gamepad key assignment]
   a1 -->> -: forward, +:backward
   a2 -->> -: left,    +:right
   b6+b7-> FORCE STOP
  */
  var buf      = new Buffer(1);
  var parsedGP = JSON.parse(gp);
  buf[0] = 0x00;

  if ( parsedGP.a1 <= -0.8 ) {
    buf[0] = buf[0] | 0x80;
  } else if( parsedGP.a1 >= 0.8 ) {
    buf[0] = buf[0] | 0x40;
  }
  if ( parsedGP.a2 <= -0.8 ) {
    buf[0] = buf[0] | 0x20;
  } else if( parsedGP.a2 >= 0.8 ) {
    buf[0] = buf[0] | 0x10;
  }

  //Force STOP
  if ( (parsedGP.b6 == 1) & (parsedGP.b7 == 1) ){
    buf[0] = 0x01;
  }
  return buf;
}

app.get('/', function(req, res){
  if(req.url == '/favicon.ico'){
    return;
  }
  res.sendFile(__dirname + '/DCconsole.html');
});
io.on('connection', function(socket){
  console.log('[user connected]');
  socket.on('disconnect', function(){
    console.log('[user disconnected]');
  });
  socket.on('gpFromClient', function(msg){
    var buf;
    io.emit('gpFromSrv', msg);
    if ( (Date.now() - last) >= interval ){
      last = Date.now();
      buf  = buildByteGP(msg)
      console.log("-> emit:" + last + ">" + buf.toString('hex'));
      sp.write(buf);
    }
  });
});

sp.on('data', function(msgFromA){
  var buf = new Buffer(msgFromA);
  console.log('  <- data from Arduino+: ' + buf.toString('hex') );
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
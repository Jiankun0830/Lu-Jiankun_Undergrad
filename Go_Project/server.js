var express = require("express");
var app     = express();
var path = require("path");
var bodyParser = require('body-parser');
var spawn = require('child_process').spawn;
var readline = require('readline');

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

var child = spawn('python', ['compute_input.py']);

child.stdin.setEncoding('utf-8');
child.stdout.setEncoding('utf-8');


app.get('/',function(req,res){
  res.sendFile(path.join(__dirname, 'public', 'WeiqiOnline.html'));
  //__dirname : It will resolve to your project folder.
});

app.get('/favicon.ico', function(req, res) {
    res.sendStatus(204);
});

app.post('/', function(req, res){    
    var message = req.body.message;       
    
    // if the program needs input on stdin, you can write to it immediately    
    child.stdin.write(message + '\n');     
    console.log(message);
    

    console.log("Hello from server!")
  

    child.stdout.once('data', function(data){   
      
      console.log(data);      
      res.end(data);
    });
    
    //child.stdout.on('end', function(){
    //  console.log('Script output =', dataString);
    //});

});

app.listen(8080);

console.log("Running at Port 8080");


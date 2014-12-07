# -*- coding: utf-8 -*-
import socket, sys
from time import strftime, localtime

host = 'localhost'
port = 8080
www_dir = 'www'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Launching HTTP server on", host, ":",port
try:
    sock.bind((host, port))
    work = True
    print "Server successfully acquired the socket with port:", port
except:
    work = False
    print "Port is not free."
print '===================================================================='

def generate_headers(code):
    header_server = 'Server: Simple-Python-HTTP-Server\n'
    header_connection = 'Connection: close\n\n'

    if  code == 200:
        h = 'HTTP/1.1 200 OK\n'
    elif code == 404:
        h = 'HTTP/1.1 404 Not Found\n'
    return h + 'Date: ' + str(strftime("%a, %d %b %Y %H:%M:%S", localtime())) +'\n' + header_server + header_connection

def shutdown():
    global work, sock
    try:
        print "Shutting down the server"
        work = False
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit()
    except Exception as e:
        print "Warning: could not shut down the socket. Maybe it was already closed? " + str(e)

def send_response(string, conn):
    global work
    request_method = string.split(' ')[0]
    print "Request body:\n\t", string.replace('\n', '\n\t')
    print "Request body end."

    if request_method == 'GET':
        file_requested = string.split(' ')[1].split('?')[0]

        print 'request:',file_requested

        if (file_requested == '/'):
            file_requested = '/index.html'
        if file_requested == '/close':
            file_requested += '.html'
            print 'shutdown'
            work = False

        file_requested = www_dir + file_requested
        print "Serving web page [",file_requested,"]"
        ## Load file content
        try:
            file_handler = open(file_requested,'rb')
            response_content = file_handler.read()
            file_handler.close()
            response_headers = generate_headers(200)
        except Exception as e:
            print "Warning, file not found. Serving response code 404\n"
            response_headers = generate_headers( 404)
            response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
        data = response_headers.encode() + response_content
        conn.send(data)
        print "Closing connection with client"
        conn.close()
    else:
        print "Unknown HTTP request method:", request_method

sock.listen(3)
while work:
    print 'waiting... '
    conn, addr = sock.accept()
    print "Got connection from:", addr
    data = conn.recv(1024)
    send_response(bytes.decode(data), conn)
    print '--------------------------------------------------------------------------------'

print 'Good bye =)'
shutdown()

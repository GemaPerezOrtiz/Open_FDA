import web6
import socketserver
##
#WEB SERVER
###
PORT = 8006
#Handler = http.server.SimpleHTTPRequestHandler
Handler = web6.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler) #controlamos la petcion con el handler
print('serving at port',PORT)
httpd.serve_forever()

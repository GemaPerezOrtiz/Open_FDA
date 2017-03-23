#web_server_FDA

import web
import socketserver
##
#WEB SERVER
###
PORT = 8000
#Handler = http.server.SimpleHTTPRequestHandler
Handler = web.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler) #controlamos la petcion con el handler
print('serving at port',PORT)
httpd.serve_forever()

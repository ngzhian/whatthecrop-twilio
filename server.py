# import os
# try:
#   from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
#   from SocketServer import TCPServer as Server
# except ImportError:
#   from http.server import SimpleHTTPRequestHandler as Handler
#   from http.server import HTTPServer as Server

# # Read port selected by the cloud for our application
# PORT = int(os.getenv('VCAP_APP_PORT', 8080))
# # Change current directory to avoid exposure of control files
# os.chdir('static')

# httpd = Server(("", PORT), Handler)
# try:
#   print("Start serving at port %i" % PORT)
#   httpd.serve_forever()
# except KeyboardInterrupt:
#   pass
# httpd.server_close()

import os

import django
from django.conf import settings
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = 'whatthecrop.settings'

django.setup()

PORT = int(os.getenv('VCAP_APP_PORT', 8080))
call_command('runserver', str(PORT), settings='whatthecrop.settings')

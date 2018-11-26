from wsgiref import simple_server
import falcon

##### Security Hardening #####
from wsgiref.simple_server import ServerHandler
ServerHandler.server_software = ("")

### Import API Classes ###
from alive import Alive

def run():
    ### Import API Classes ###
    alive = Alive()
    ### Build API Server ###
    app = falcon.API()
    app.add_route('/alive', alive)
    ### Run Server ###
    httpd = simple_server.make_server('0.0.0.0', 8444, app)
    httpd.serve_forever()

def main():
    run()

if __name__ == "__main__":
    main()

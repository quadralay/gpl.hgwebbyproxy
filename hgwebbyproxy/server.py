from .wsgi import HGWebByProxy
import sys
import waitress


if __name__ == "__main__":
    if len(sys.argv) == 4:
        # Create application
        #
        hgwebbyproxy_app = HGWebByProxy()

        # Configure server
        #
        server_name = sys.argv[1]
        server_host = sys.argv[2]
        server_port = int(sys.argv[3])

        # Launch server
        #
        waitress.serve(hgwebbyproxy_app, host=server_host, port=server_port)

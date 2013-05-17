import wsgi
import sys
import rocket


if __name__ == '__main__':
    try:
        if (len(sys.argv) == 4):
            # Create application
            #
            hgwebbyproxy_app = wsgi.HGWebByProxy()

            # Configure server
            #
            server_name = sys.argv[1]
            server_host = sys.argv[2]
            server_port = int(sys.argv[3])
            server = rocket.Rocket((server_host, server_port), 'wsgi', {'wsgi_app': hgwebbyproxy_app}, 10, 25, 5, 600)

            server.start()

    except KeyboardInterrupt:
        server.stop()

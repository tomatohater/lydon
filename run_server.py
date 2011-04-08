'''
Run Lydon on built-in Flask server. Mostly for developent and debugging.
'''
import optparse

from lydon import app


if __name__ == '__main__':
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("--host", dest="host", default='127.0.0.1', type="string",
                      help="the hostname to listen on. set this to '0.0.0.0' " \
                           "to have the server available externally as well.")
    parser.add_option("--port", dest="port", default=5000, type="int",
                      help="the port of the webserver")
    (options, args) = parser.parse_args()

    app.run(host=options.host, port=options.port)
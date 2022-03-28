# app.py

from flask import Flask
import time

if __name__ == '__main__':
    app = Flask(__name__)
    import Modules.umbrella
    import Modules.amp4e

    while True:
        try:
            app.run(threaded=True, host='172.17.0.1', port=5000) #Listen on the docker nic from SXO Connector
#            app.run(threaded=True, port=5555) #Debug
        except OSError as error: #Wait for docker service to finish
            if error.errno == 49:
                time.sleep(5)
                continue

import sys
import os
import subprocess

from logbook import app

DEBUG_MODE = "--debug" in sys.argv

env = os.environ
if not DEBUG_MODE:
    env = {**os.environ, "NODE_ENV": "production"}

subprocess.Popen("npm run build-css", env=env, shell=True).wait()

if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug=DEBUG_MODE)

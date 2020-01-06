import sys

from logbook import app

if __name__ == "__main__":
    app.run("127.0.0.1", port=5000, debug="--debug" in sys.argv)

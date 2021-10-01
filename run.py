from flask import Flask
# Run a test server.
from app import create_app
create_app().run(debug=True)
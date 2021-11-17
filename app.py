"""
Main Module: This file is start point to run project, all routes availabe and swagger route defined here
"""
from flask import redirect

import config

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# Default Route
@connex_app.route("/")
def home():
    return redirect("/api/ui")

if __name__ == "__main__":
    connex_app.run(host='localhost', port=5000, debug=True)
"""Main entry for the web application.

This file needs to be not named __main__ because it causes issues with Gunicorn.
"""

import os

from personal.app_tornado import App

PORT = int(os.environ.get("PORT", 8080))

app = App()

if __name__ == "__main__":
    app.serve(port=PORT)

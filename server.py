"""
The Server file. Hosts the server.
"""
# Third Party Imports
from flask import render_template

# Custom Imports
import core
from planner_logger import add_to_log

@core.app.route('/')
def index():
    """
    The index page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    add_to_log('[INFO] Starting server!')
    core.app.run('0.0.0.0', 5000, debug=True)

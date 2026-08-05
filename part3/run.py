import os
from app import create_app
from config import config

# Get the current environment mode from system variables or default to 'development'
env_name = os.getenv('FLASK_ENV', 'development')

# Create the Flask application instance using the designated configuration
app = create_app(config.get(env_name, config['default']))

if __name__ == '__main__':
    # Start the Flask development server on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)

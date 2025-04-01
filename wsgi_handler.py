from app import app  # Import your Flask app
from serverless_wsgi import handle

def handler(event, context):
    return handle(event, context)

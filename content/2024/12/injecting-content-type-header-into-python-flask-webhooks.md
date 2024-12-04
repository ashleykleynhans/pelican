Title: Injecting Content-Type Header into Python Flask Webhooks
Date: 2024-12-04
Author: Ashley Kleynhans
Modified: 2024-12-04
Category: DevOps
Tags: python, flask, webhooks
Summary: This post helps you to automatically inject missing
    `Content-Type` headers into your Python Flask Webhooks.
Status: Published


## Introduction

We recently had an issue where one of our 3rd party providers decided
that it would be a good idea to remove the `Content-Type` header
from the webhooks that they send to our application, breaking the
contract of the webhook format.

Our application relies heavily on the webhooks for receiving status
updates and the output from the 3rd party application, and our
customers were negatively impacted by this unannounced change.

## Automatically injecting the missing Content-Type headers

Fortunately, it is possible to implement a simple work-around
for this issue in a Python Flask application as follows:

```python
@app.before_request
def before_request():
    # Only handle POST requests to /webhook endpoints
    if request.method == 'POST' and '/webhook/' in request.path:
        content_type = request.headers.get('Content-Type', '')

        # If Content-Type is not set or is not application/json
        if 'application/json' not in content_type.lower():
            # Try to parse the data as JSON
            try:
                # Force Flask to parse JSON data even if Content-Type is not set
                if request.data:
                    request.get_json(force=True)
                # Modify the request headers to include Content-Type
                request.environ['CONTENT_TYPE'] = 'application/json'
            except Exception as e:
                # If JSON parsing fails, return 400 Bad Request
                return make_response(jsonify({
                    'stage': 'self',
                    'status': 'error',
                    'msg': 'Invalid JSON data',
                    'detail': str(e)
                }), 400)
```
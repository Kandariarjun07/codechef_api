import json

def handler(event, context):
    """
    Simple test function to verify Netlify Functions are working
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': 'Hello from Netlify Functions!',
            'event': event,
            'context': str(context)
        })
    }

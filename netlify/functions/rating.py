import json
import re
import requests

def get_codechef_data(username):
    """
    Fetches a user's profile page and extracts the embedded rating data JSON.
    """
    url = f"https://www.codechef.com/users/{username}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        match = re.search(r'jQuery\.extend\(Drupal\.settings, (\{.*\})\);', response.text)
        if not match:
            return None, "Could not find data object in page source."
            
        data = json.loads(match.group(1))
        return data, None
        
    except requests.exceptions.HTTPError:
        return None, f"User '{username}' not found or profile is private."
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

def handler(event, context):
    """
    This is the main entry point for the Netlify Function.
    It processes the incoming request and returns a JSON response.
    """
    # Handle case where queryStringParameters might be None
    query_params = event.get('queryStringParameters') or {}
    username = query_params.get('username')

    # --- THIS IS THE MODIFIED LOGIC ---
    # If no username is provided (which happens when the root URL is hit),
    # return a helpful welcome message instead of an error.
    if not username:
        welcome_message = {
            "message": "Welcome to the Unofficial CodeChef Rating API!",
            "usage": "To get a user's rating, use the /user/<username> path.",
            "example": "https://<your-site-name>.netlify.app/user/gennady"
        }
        return {
            'statusCode': 200, # Return 200 OK
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(welcome_message, indent=2)
        }

    # The rest of the function continues as before if a username is present
    user_data, error = get_codechef_data(username)

    if error:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': error})
        }

    try:
        rating_history = user_data.get("date_versus_rating", {}).get("all", [])
        
        if not rating_history:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'username': username, 'status': 'Unrated', 'currentRating': 0, 'peakRating': 0})
            }

        latest_contest = rating_history[-1]
        current_rating = int(latest_contest['rating'])
        all_ratings = [int(contest['rating']) for contest in rating_history]
        peak_rating = max(all_ratings)

        response_body = {
            'username': username,
            'status': 'Success',
            'currentRating': current_rating,
            'peakRating': peak_rating,
            'ratingHistory': rating_history
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response_body)
        }
        
    except (KeyError, IndexError, ValueError):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Failed to parse user rating data from page.'})
        }
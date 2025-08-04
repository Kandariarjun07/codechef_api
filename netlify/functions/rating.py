import json
import re
import requests

def get_codechef_data(username):
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
    username = event.get('queryStringParameters', {}).get('username')

    if not username:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Username parameter is required.'})
        }

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
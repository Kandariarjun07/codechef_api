# CodeChef Rating API

A simple, unofficial serverless API deployed on Netlify to fetch a user's current and peak rating from CodeChef. It works by parsing the embedded JSON data on a user's profile page, making it more reliable than traditional web scraping of visual HTML elements.

## How to Use the Live API

To use the deployed API, make a GET request to the following endpoint with a user's CodeChef handle.

**Endpoint:**
```
https://<your-netlify-site-name>.netlify.app/api/rating
```

**Query Parameter:**
- `username` (Required): The CodeChef username you want to look up.

### Example Request

Replace `<your-netlify-site-name>` with the URL provided by Netlify after deployment.

```
https://your-app.netlify.app/api/rating?username=gennady
```

### Example Success Response (200 OK)

```json
{
  "username": "gennady",
  "status": "Success",
  "currentRating": 3878,
  "peakRating": 3878,
  "ratingHistory": [
    {
      "code": "COOK01",
      "getyear": "2010",
      "getmonth": "9",
      "getday": "26",
      "rating": "1738"
    },
    {
      "code": "START175A",
      "getyear": "2025",
      "getmonth": "2",
      "getday": "26",
      "rating": "3878"
    }
  ]
}
```

### Example Error Response (404 Not Found)

```json
{
  "error": "User 'non_existent_user_123' not found or profile is private."
}
```

## Data Structure

The API returns a JSON object with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `username` | String | The requested CodeChef username. |
| `status` | String | Success, Unrated, or an error status. |
| `currentRating` | Integer | The user's latest rating after their last rated contest. |
| `peakRating` | Integer | The user's highest rating achieved. |
| `ratingHistory` | Array of Objects | A list of all rated contests the user has participated in. |

## Deploy Your Own Version

You can deploy your own instance of this API in seconds.

### One-Click Deploy

Click the "Deploy to Netlify" button at the top of this README or use the link below to automatically set up the project in your own Netlify account.

### Manual Deployment

1. **Clone or Fork this Repository.**

2. **Push it to your own GitHub/GitLab account.**

3. **Connect to Netlify:** Log in to Netlify and choose "Add new site" → "Import an existing project". Select your new repository.

4. **Deploy:** Netlify will automatically detect the `netlify.toml` file and set up the build and function settings. Click "Deploy site" and you're done!

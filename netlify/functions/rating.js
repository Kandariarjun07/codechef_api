const https = require('https');

async function getCodeChefData(username) {
    return new Promise((resolve, reject) => {
        const url = `https://www.codechef.com/users/${username}`;
        const options = {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        };

        https.get(url, options, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    // Extract the JSON data from the page
                    const match = data.match(/jQuery\.extend\(Drupal\.settings, (\{.*\})\);/);
                    if (!match) {
                        reject(new Error('Could not find data object in page source'));
                        return;
                    }
                    
                    const userData = JSON.parse(match[1]);
                    resolve(userData);
                } catch (error) {
                    reject(new Error('Failed to parse user data'));
                }
            });
        }).on('error', (error) => {
            if (error.code === 'ENOTFOUND' || error.message.includes('404')) {
                reject(new Error(`User '${username}' not found or profile is private`));
            } else {
                reject(new Error(`Network error: ${error.message}`));
            }
        });
    });
}

exports.handler = async (event, context) => {
    // Set CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle preflight requests
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    try {
        // Debug: Log the entire event to see what we're receiving
        console.log('Event:', JSON.stringify(event, null, 2));

        // Get username from query parameters or path
        let username = event.queryStringParameters?.username;

        // If no username in query params, try to extract from path
        if (!username && event.path) {
            const pathMatch = event.path.match(/\/rating\/(.+)$/);
            if (pathMatch) {
                username = pathMatch[1];
            }
        }

        // If no username provided, return welcome message
        if (!username) {
            const welcomeMessage = {
                message: "Welcome to the Unofficial CodeChef Rating API!",
                usage: "To get a user's rating, use the /user/<username> path.",
                example: "https://codechefapi.netlify.app/user/gennady"
            };
            
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify(welcomeMessage, null, 2)
            };
        }

        // Fetch user data from CodeChef
        const userData = await getCodeChefData(username);
        
        // Extract rating history
        const ratingHistory = userData?.date_versus_rating?.all || [];
        
        if (ratingHistory.length === 0) {
            return {
                statusCode: 200,
                headers,
                body: JSON.stringify({
                    username: username,
                    status: 'Unrated',
                    currentRating: 0,
                    peakRating: 0
                })
            };
        }

        // Calculate current and peak ratings
        const latestContest = ratingHistory[ratingHistory.length - 1];
        const currentRating = parseInt(latestContest.rating);
        const allRatings = ratingHistory.map(contest => parseInt(contest.rating));
        const peakRating = Math.max(...allRatings);

        const responseBody = {
            username: username,
            status: 'Success',
            currentRating: currentRating,
            peakRating: peakRating,
            ratingHistory: ratingHistory
        };

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify(responseBody)
        };

    } catch (error) {
        console.error('Error:', error.message);
        
        return {
            statusCode: 404,
            headers,
            body: JSON.stringify({
                error: error.message
            })
        };
    }
};

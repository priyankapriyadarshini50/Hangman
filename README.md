Application
-----------------------
The whole Hangman game application has a 'decoupled architecture'
Django Rest Framework based APIs has been used to power the frontend for a hangman game developed in Vuejs
PostgresSQL is used as backend database (sqllite can be used).
* This app exposes an API with the following endpoints. All requests and responses use the JSON data type.  
* Django backend Caching(Redis cache) has been implemeted to improve the performance, reduce latency and
 reduce database connection. The whole gaming logic is handles in the Redis cache.  
* Also, I have followed object oriented programming structure for better
code modularity and reusability.
* Added django logging for production ready and for better troubleshooting.  
* Hybrid JWT secure cookie based Authentication is implemented to secure the rest APIs endpoints and user is 
able to securly login and play games and logout of the application.
* Store the refresh token in an HttpOnly cookie (protected from JS access)
* I have set authentication middleware to accept and validate the cookies

New game
-----------------------
The api/game/new/ endpoint starts a new game. It assigns a random word from the list of following words for the player to guess:
["Hangman", "Python", "Django", "Bottle", "Data"]
The player are allowed to guess incorrectly the number of characters in the word. So for example if the selected word in "Django", 
the player can make 5 incorrect guesses before loosing the game.
This endpoint should return the id of the newly created game object.

Game state
------------------------
The api/game/<:id>/ endpoint accepts a game id and returns a state which contains:
The current state of the game. InProgress , Lost , or Won .

Guess
--------------------------
The api/game/<:id>/guess/ endpoint accepts a single character in JSON format 
{
"guess_letter": "e"
}
and return both the game state as defined in the Game state endpoint and if the guess was correct or not.

![A game status image](./static/game_status_image.png)

Register a user
-----------------------
The api/users/register/ endpoint allow users to register and returns Users data with 200 OK status

Login a user
-----------------------
The api/users/login/ endpoint allow users to login to application after verifying the credentials 
and returns users info in JSON format with token as cookies

Logout a user
-----------------------
The api/users/logout/ endpoint allow users to logout from application after deleting the tokens 
and returns a success message in JSON format

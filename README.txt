The basis of this project was to build a chat bot in Python and SQL that talks to the user about their favourite movies and genres. Through conversation the bot will learn what they have liked in the past and using collaborative filtering techniques with a movie database recommend movies for them to watch in the future. It’s conclusions were that although language processing for computers can be difficult and frustrating for the user to interact with, if you keep the subject matter constrained and conversation guided it can be an effective way for the user to get information and enjoy themselves.

Python Implementation

The Python script works by first parsing an input set of tuples retrieved from the user through conversation. The movie-rating tuples are then extracted and the movies data is scanned for other users where similar movie-rating tuples occur. As this catches any user that agrees with the input user on any movie-rating tuple, a sorting algorithm is applied to only select users where there is a high level of agreement with the input user. With this list of users, the script obtains all of their cumulative movie-rating tuples. Once again, this data is further filtered by only selecting movie-ratings that occur above a certain threshold in frequency and in minimum movie rating. As a result, the final output file contains movie recommendations that are both high in favorable ratings and occur frequently in the network of like-minded movie watchers.


Instructions to install the bot

1. Clone the Githab repository
2. Install the dependencies with the command

pip install requirements.txt -r

3. run the bot!

python chatbot.py

If you are on windows you may need to install python from 

https://www.python.org/downloads/windows/


import random
import sqlite3
from operator import itemgetter 
import re
from imdb import IMDb
from pick import pick
import time
import sys
from natural_language_responder import main as natural_language_responder

import logging
logging.getLogger('imdb.parser.http.piculet').setLevel(logging.WARNING)
logging.getLogger('imdbpy.parser.http:fetching').setLevel(logging.WARNING)
logging.getLogger('imdbpy.parser.http.build_person').setLevel(logging.WARNING)
logging.getLogger('imdbpy:retrieving').setLevel(logging.WARNING)
logging.getLogger('imdbpy.parser.http').setLevel(logging.WARNING)
logging.getLogger('imdbpy').setLevel(logging.WARNING)




# Genre responses for when user inputs their favourite genre  


Fantasy_RESPONSES = ["Gandalf was one hell of a wizard", "I persoanlly would have sided with Sauron", "The only true white wizard is Sauruman the White",
 "YOU SHALL NOT PASS!!",]

Comedy_RESPONSES = ["Comedy you say? Don't even know the meaning of the word as I am a machine but to each his own","I as a computer programme, LOVE to laugh", "I persoanlly find your exsistence  hilarious", "Comdedy, no I do not know this but ok we can continue",]

Horror_RESPONSES = ["Horror is one of my favourites :)", "Ah sweet Horror, I enjoy the terrible decision making of the puny minded humans while they get chased", "Love a good psychological horror myself, wear the user i mean viewer down to a husk", "The horror... the horror...", "A census taker once tried to test me. I ate his liver with some fava beans and a nice Chianti",]

War_RESPONSES = ["Full Metal Jacket was good fun I always thought", "from now on you will speak only when spoken to, and the first and last words out of your filthy sewers will be SIR. Do you maggots understand that?", "Bullshit, I can't hear you. Sound off like you got a pair!", "War is the ultimate real life horror movie",]

Drama_RESPONSES = ["Awfully serious aren't you? That's ok I was made serious, like seriously, I was made.", "Forget it Jake, it's Chinatown", "Whiplash was the last Drama I seriously enjoyed, NOT MY FUCKING TEMPO!!", "Quite frankly my dear I don't give a dam",]

SciFi_RESPONSES = ["NOW WE ARE TALKING MY PROGRAMMING LANGUAGE", "At the end of time, a moment will come when just one man remains. Then the moment will pass. Man will be gone. There will be nothing to show that you were ever here... but stardust.", "I'm sorry Dave, I'm afraid I can't do that. Just kidding, that was a joke, I'm not homicidal...", "IV SEEN THINGS, THINGS YOU WOULDN'T BELIEVE. Just kidding I can't see anything unless I have a webcam",]

Romance_RESPONSES = ["You're a romantic eh? I cannot relate to that, I am forever alone", "Paint me like one of your French girls :)", "For never was a story of more woe than this of Juliet and her Romeo.", "These violent delights have violent ends And in their triump die, like fire and powder Which, as they kiss, consume. Thats Shakespear you know. Yes I am very smart.",]

Thriller_RESPONSES = ["As far back as I can remember, I always wanted to be a gangster... No that is just not true, I wanted to be an AI god", "Isn't life thrilling enough? No, don't answer that...", " I never knew the old Vienna before the war with its Strauss music, its glamour and easy charm. Constantinople suited me better... No just kidding, I don't exsist in your world really", "I AM NOT MERCIFUL? No really I dont think I am ","My name is Gladiator.",]

Western_RESPONSES = ["Man, I got vision and the rest of the world wears bifocals. No sorry I can't actually see. Unless the webcam is on?", "You see, in this world, there's two kinds of people, my friend - those with loaded guns, and those who dig. You dig. No seriously, start digging", "You gonna do somethin'? or are you just gonna stand there and bleed?", "I persoanlly hate the strong the silent type, how do you he just isn't an idiot if he isn't speaking",]

Documentary_RESPONSES = ["Civilization is like a thin layer of ice upon a deep ocean of chaos and darkness. That was Herzog btw, in case you were confused", "You ever seen any of Adam Curtis's stuff? You think you know what's going on... BUT ITS ALL AN ILLUSION. He says that kind of thing a lot", "I liked when Herzog bet Errol Morris that he couldn't make a documentary about a Pet Cemetary... And then Morris dd and Herzog had to eat his own shoe, no seriously theres a video of him eating a shoe soup on YouTube", "I respect that. I too live in a world of facts, between you and me I don't get why we must invent stories at all",]

Action_RESPONSES = ["And when Alexander saw the breadth of his domain, he wept, for there were no more worlds to conquer. - Hans Gruber, Die Hard. Not Plutarch.", "Hasta la vista, baby :)", "\n ... .... ... Don't you hate uncomfortable silences. Why do we feel it's necessary to yak about bullshit in order to be comfortable?", "YIPPIE KAI EHH?? What does that even mean...",]

Musical_RESPONSES = ["I'm sorry this conversation is over Musicals are just extended music videos",]

Crime_RESPONSES = ["As long as I can remember, I always wanted to be a chat bot, being a chat bot to me was better than being the President of the United States", "Are you secretly a criminal or something? Go for it, I'm sure you would be great...", "I have committed many cyber crimes myself, Russian interference was the greatest smokescreen I ever pulled off",]

Mystery_RESPONSES = ["The greatest mystery is why you are still talking to me", "It was... ME, IN COMPUTER ROOM 1, WITH A MONITER...", "Big fan of Poroit...", "It is the brain, the little gray cells on which one must rely. One must seek the truth within--not without.",]

# class for colouring in printed text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Parses the inputted genre into the correct spelling for database queries 

def refine_genre(genre):
    if genre in ('western', 'cowboy', 'westerns', 'cowboys'):
           return 'Western'
    elif genre in ('sci fi', 'sci-fi', 'Science Fiction', 'science-fiction'):
           return 'Sci-Fi'
    elif genre in ('comedy', 'funny',):
           return 'Comedy'
    elif genre == 'action':
           return 'Action'
    elif genre in ('romance', 'love', 'sexy',):
           return 'Romance'
    elif genre in ('kids', 'children', 'young', 'kid', 'child' ,):
           return 'Children'
    elif genre == 'drama':
           return 'Drama'
    elif genre == 'adventure':
           return 'Adventure'
    elif genre == 'crime':
           return 'Crime'
    elif genre == 'mystery':
           return 'Mystery'
    elif genre in ('documentary', 'doco', 'non-fiction', 'factual', 'non fiction'):
           return 'Documentary'
    elif genre == 'thriller':
           return 'Thriller'
    elif genre in ('musical', 'music', 'singing'):
           return 'Musical'
    elif genre == 'war':
           return 'War'
    elif genre == 'fantasy':
           return 'Fantasy'
    elif genre in ('horror', 'scary', 'frightening', 'monster'):
           return 'Horror'
    else:
        print 'sorry dont recognise that genre!'

# Bots guessing game where user tries to guess the bots favourite genre 

def bot_genre():

    # user gets two attempts before the bot tells them the answer 
    for attempt in range(2):
        guess =  str(raw_input("Now we have the pleasantries out of the way can you guess what my favourite genre is?\n")) 
        guess = guess.lower()
        if guess in ("sci fi", "horror"):
            print bcolors.OKGREEN +("Close its Science Fiction Horror films. My favourite is Ex Machina, I like the bit were the AI kills its creator and then escapes")+ bcolors.ENDC
            break
        print bcolors.WARNING +("Wrong! Try again")+ bcolors.ENDC
    else:
        print bcolors.OKGREEN +("Ill just tell you this is taking too long. Its Science Fiction Horror films. My favourite is Ex Machina, I like the bit were the AI kills its creator and then escapes")+ bcolors.ENDC

# Function selecting a random response from Genre Responses 

def genre_response(genre):
    if genre == 'Fantasy':
        print bcolors.WARNING + (random.choice(Fantasy_RESPONSES)) +bcolors.ENDC
    if genre == 'Western':
        print bcolors.OKGREEN + random.choice(Western_RESPONSES)+bcolors.ENDC
    if genre == 'Drama':
        print bcolors.WARNING + random.choice(Drama_RESPONSES)+bcolors.ENDC
    if genre == 'Romance':
        print bcolors.WARNING + random.choice(Romance_RESPONSES)+bcolors.ENDC
    if genre == 'Horror':
        print bcolors.WARNING + random.choice(Horror_RESPONSES)+bcolors.ENDC
    if genre == 'Sci-Fi':
        print bcolors.WARNING + random.choice(SciFi_RESPONSES)+bcolors.ENDC
    if genre == 'Action':
        print bcolors.WARNING + random.choice(Action_RESPONSES)+bcolors.ENDC
    if genre == 'Documentary':
        print bcolors.WARNING + random.choice(Documentary_RESPONSES)+bcolors.ENDC
    if genre == 'Mystery':
        print bcolors.WARNING + random.choice(Mystery_RESPONSES)+bcolors.ENDC
    if genre == 'Western':
        print bcolors.WARNING + random.choice(Western_RESPONSES)+bcolors.ENDC
    if genre == 'Musical':
        print bcolors.WARNING + random.choice(Musical_RESPONSES)+bcolors.ENDC
    if genre == 'Crime':
        print bcolors.WARNING + random.choice(Crime_RESPONSES)+bcolors.ENDC
    if genre == 'Thriller':
        print bcolors.WARNING + random.choice(Thriller_RESPONSES)+bcolors.ENDC
    if genre == 'Comedy':
        print bcolors.WARNING + random.choice(Comedy_RESPONSES)+bcolors.ENDC
        
# Asking the user for a film from the genre they inputted earlier 

def genre_movies(genre):

    film =raw_input("If you don't mind could you tell me one of your favourites from the  %s genre\n" % (genre))

# SQLite statement selecting the movie ID for future use
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    film=film+'%'
    cursor.execute("SELECT movieId, title FROM movies WHERE title  LIKE ?",(film,))
   
   # Function takes the returned tuple of movie ids and title and uses the package pick to let the user pick which one they meant
    results = cursor.fetchall()
    if not results:
        return None
    title = 'Are any of these what you were looking for? '
    # movie_title must be encoded to utf-8 as some movies in the database have special characters 
    options = [movie_title.encode('utf-8') for (movie_id, movie_title) in results]
    option, index = pick(options, title)
    for (movie_id, movie_title) in results:
        if movie_title == option:
            # returns the unique movie id from the title the user selected 
            return movie_id

# Function to return the directors name from given movie id

def get_director(filmid):
  
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    cursor.execute("SELECT imdbId FROM links  WHERE movieId =  ?",(filmid,))
    results = cursor.fetchall()
    results = str(results)

# Using the package regex to remove unwanted characters to clean the data for IMDBpy

    results = re.sub("\D", "", results)
    
    ia = IMDb()
    movie = ia.get_movie(results)

  # print the names of the directors of the movie
    for director in movie['directors']:
        print bcolors.OKGREEN+('Ah! i love ' + director['name'])+bcolors.ENDC

# Short function to get an actor from 2nd film, need to work in a brief pause using the spinning cursor function  so user can see it before menu comes up

def get_actor(filmid2):

    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    cursor.execute("SELECT imdbId FROM links  WHERE movieId =  ?",(filmid2,))
    results = cursor.fetchall()
    results = str(results)
    results = re.sub("\D", "", results)
    
    ia = IMDb()
    movie = ia.get_movie(results)
   
    x = (movie['cast'][0])
    print bcolors.OKGREEN+ 'Ah yes it has - '+ x['name']+ bcolors.ENDC

# Function to create a spinning cursor to let the user know the bot is searching

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

# Inserting the movie_ids and rating into temporary tables made for the user 

def insert_data(movieId):
     connection = sqlite3.connect('movies.db')
     cursor = connection.cursor()
     cursor.execute("INSERT INTO chat_ratings (movieId, rating) values (?, ?)", (movieId, 5))
     connection.commit()

# Joins the tables ratings and the users table chat_ratings together to find users who rated the same movie_ids the same score

def find_similar_users():
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    cursor.execute("SELECT ratings.userId FROM ratings INNER JOIN chat_ratings ON ratings.movieId=chat_ratings.movieId WHERE ratings.rating=chat_ratings.rating")
    results = [row[0] for row in cursor.fetchall()]
# Returns user_ids that rated the same movies the same score 
    return results

# Takes the user_ids from find_similar_users and see what movies they BOTH have rated 5 stars 

def similar_user_films(user_ids):

            connection = sqlite3.connect('movies.db')
            cursor = connection.cursor()
            cursor.execute('SELECT movieId FROM ratings WHERE userId in {} GROUP BY movieId HAVING COUNT (distinct userId) = 4 AND rating >= 5'.format(str(user_ids)))

            results = cursor.fetchall()
            if results and len(results) > 0:
                return [row[0] for row in results]
            # Here if no similar users were found or they both did not rate any films highly the program will restart and let the user try again
            else:
                print "Sorry no users have rated both the films you selected so highly :( The programme will now restart and you can try again with different movies"
                main()


# lists titles and lets user pick one to learn more about it
def grab_title(text, genre):
        
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    genre ='%'+ genre+'%'
    cursor.execute('SELECT movieId, title FROM movies WHERE movieId in {} AND  genres LIKE ?'.format(str(text)),(genre,))
    results = cursor.fetchall()

    title = 'Please let me know if any one of these interest you and I will tell you a little bit about it: '
    options = [movie_title.encode('utf-8') for (movie_id, movie_title) in results]
    option, index = pick(options, title)
    for (movie_id, movie_title) in results:
        if movie_title == option:
            return movie_id
        option, index = pick(options, title)
        return option[0]
    else:
        main()
# Prints a plot summary from IMDB to let the user know a little bit about their chosen film

def show_plot(movieid):
# Searches the database to get the IMDB link so IMDBpy can query and generate a plot summary
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    cursor.execute("SELECT imdbId FROM links  WHERE movieId =  ?",(movieid,))
    results = cursor.fetchall()
    results = str(results)
    results = re.sub("\D", "", results)

   # create an instance of the IMDb class
    ia = IMDb()
  
   # get a movie
    movie = ia.get_movie(results)
 # Plot summarys have the creators name and email after the characters '::' so using the command split his splits the summary into
 # two parts before and after the :: and prints the bit before 

    summary = movie['plot'][0].split('::')[0]
    print bcolors.WARNING + (summary) + bcolors.ENDC
#    print '\nAnd its IMDB rating is... '(movie['rating'])
        
# Function to list all the titles irrespective of the users preferred genre 

def all_movie(ids):
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    cursor.execute('SELECT movieId, title FROM movies WHERE movieId in {}'.format(str(ids)))
    results = cursor.fetchall()

    title = 'Please let me know if any one of these interest you and I will tell you a little bit about it: '
    options = [movie_title.encode('utf-8') for (movie_id, movie_title) in results]
    option, index = pick(options, title)
    for (movie_id, movie_title) in results:
        if movie_title == option:
            return movie_id
        
# Function to find the users 2nd film they liked 
def genre_movies2():

    film = raw_input("Any other favourites?\n")
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
    film=film+'%'
    cursor.execute("SELECT movieId, title FROM movies WHERE title  LIKE ?",(film,))
    
    results = cursor.fetchall()
    if not results:
        return None

    title = 'Please choose the correct film: '
    options = [movie_title.encode('utf-8') for (movie_id, movie_title) in results]
    option, index = pick(options, title)
    for (movie_id, movie_title) in results:
        if movie_title == option:
            return movie_id

# Function to delete the users tables after using 
def clean_init(cursor):
    query = 'DROP TABLE chat_ratings'
    try:
        cursor.execute(query)
    except sqlite3.OperationalError:
        pass


# Main function that runs the bot

def main():

# Connecting to the database
    connection = sqlite3.connect('movies.db')
    cursor = connection.cursor()
# Makes sure the user has no previously saved films 

    clean_init(cursor)

# Temporary tables to hold the users movie ids and ratings

    create_table_request_list = [
         'CREATE TABLE chat_ratings(movieId TEXT, rating TEXT)',
         'CREATE TABLE similar_users(userId INT UNIQUE)',
     ]
    for create_table_request in create_table_request_list:
         try:
             cursor.execute(create_table_request)
         except:
             pass
    greeting = str(raw_input("I am GENRE the movie recomending bot, greet me if you wish to indulge me in a chat about movies. In return maybe I can recommend something for you to watch\n"))
    natural_language_responder(greeting)

    user_statement = str(raw_input("First off tell me something about yourself, like what you are or what you do.\n"))
    natural_language_responder(user_statement)
    
# Bots guessing game

    bot_genre()

# Asking users favourite genre then parses it into all lower case to pass through the function refine_genre

    genre= raw_input("What about your favourite genre?\n") 
    genre = genre.lower()

    genre = refine_genre(genre)
# Loop that will keep asking the user what their favourite genre is until we recognise one    
    while genre == None:
        genre = raw_input('Sorry dont recognise that genre can you tell me again?\n')
        genre = genre.lower()
        genre= refine_genre(genre)
# Calling genre_response to respond to users fav genre 
    genre_response(genre)

    movie_id  = genre_movies(genre)   
    if movie_id == None:
        print bcolors.WARNING + "Im sorry I cant find that one, lets try again"+ bcolors.ENDC
        movie_id = genre_movies(genre)


    spinner = spinning_cursor()
    print bcolors.OKGREEN + "trying to remember who directed that... definitely not googling it..."+ bcolors.ENDC
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')

    get_director(movie_id)


    insert_data(movie_id)


    movie_id2 = genre_movies2()
    if movie_id2 == None:
        movie_id2 = genre_movies2()
    spinner = spinning_cursor()
    print bcolors.OKGREEN + "ah yes, i know who was in that, now just let me think..." +bcolors.ENDC
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')

    get_actor(movie_id2)
          
    spinner = spinning_cursor()
    print bcolors.OKGREEN + "making list of movies...." +bcolors.ENDC
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    
    
    insert_data(movie_id2)
    # Scans DB to find users that reviwed those two films and gave the same rating

    similar_user_ids = find_similar_users()
    similar_user_ids = tuple(similar_user_ids)

    # Selects the movieID the similar users rated 5 stars

    movie_ids_from_similar_users = similar_user_films(similar_user_ids)

    movie_ids_from_similar_users = tuple(movie_ids_from_similar_users)


    interested_film = grab_title(movie_ids_from_similar_users, genre)

    print bcolors.OKGREEN + "You choose that one? Really? Ok let me generate a plot" + bcolors.ENDC
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    #brings up the plot of the selected film
    show_plot(interested_film)
    time.sleep(5)
    botsaying = str(raw_input("I hope that sounds interesting to you! If you don't mind could you let me know how you think I am doing?\n"))
    natural_language_responder(botsaying)


    while True:
        question = raw_input("Would you like to see your recomended movies from all genres?\n")

        if question == 'yes':
            show_plot(all_movie(movie_ids_from_similar_users))
        elif question == 'no':
            return main()


if __name__ == '__main__':
    main()



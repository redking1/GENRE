from __future__ import print_function, unicode_literals
import random
import os
import sys

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob
from config import FILTER_WORDS

Greetings = ("hello","hey", "hi", "greetings", "sup", "what's up",)

Respond_to_greeting_phrases = ["Hello Clarice.", "Hello. My name is Inigo Montoya. You killed my father. Prepare to die", "Say hello to my little friend", 
 "Good morning! And in case I don't see ya, good afternoon, good evening and goodnight!",]
# Checks for greeting then randomly selects a greeting response from Respond_to_greeting_phrases
def greeting_check(sentence):
    for word in sentence.words:
        if word.lower() in Greetings:
            return random.choice(Respond_to_greeting_phrases)

# Sentences we'll respond with if we have no idea what the user just said

Response_for_when_bot_doesnt_understand = [
    "There is no spoon",
    "Im sorry Hal, I can't do that",
    "ET phone home",
    ]

# If the user tries to tell us something about ourselves, use one of these responses

Bot_responding_about_itself = [
    "You're just jealous",
    "I worked really hard on that",
    "If i were to rate myself on IMDB i would be {} stars".format(random.randint(100, 500)),
]

# Raises exception if users says something on the filter list
class Filter_bad_words(Exception):
    pass

# Check for pronouns to respond with A or An
def check_for_vowels(word):
    return True if word[0] in 'aeiou' else False


# Main loop. Read sentence and choose response
def film_response(sentence):
    resp = respond(sentence)
    return resp

# Find relevant pronoun in input sentence, wont be any if none are there
def identify_pronouns(sent):
    pronoun = None
# PRP = pronoun
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'PRP' and word.lower() == 'you':
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            pronoun = 'You'
    return pronoun
# end

# Find the verb in the sentence
# VB = verb
def identify_verbs(sent):
    verb = None
    pos = None
    for word, position in sent.pos_tags:
        if position.startswith('VB'): 
            verb = word
            pos = position
            break
    return verb, pos

# Finds the noun in the sentence
# NN = noun
def identify_nouns(sent):
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':  
                noun = w
                break

    return noun

# JJ = adjective 
def identify_adjectives(sent):
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':  
            adj = w
            break
    return adj



def answer_the_user(pronoun, noun, verb):
# bot understands users input and so will respond using as much of it as possible
    resp = []

    if pronoun:
        resp.append(pronoun)

# We always tell the user they are not whatever they said they are .
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "I'm"):  
            if pronoun.lower() == 'you':
                resp.append("aren't really")
            else:
                resp.append(verb_word)
    if noun:
        pronoun = "an" if check_for_vowels(noun) else "a"
        resp.append(pronoun + " " + noun)

    resp.append(random.choice(("lol",  ", sorry", ", just kidding...")))

    return " ".join(resp)
# end


def check_for_comment_about_bot(pronoun, noun, adjective):
    """Check if the user's input was about the bot itself, in which case try to fashion a response
    that feels right based on their input. Returns the new best sentence, or None."""
    resp = None
    if pronoun == 'I' and (noun or adjective):
        if noun:
            if random.choice((True, False)):
                resp = random.choice(Verbs_with_capial_plural_nouns_about_bot).format(**{'noun': noun.pluralize().capitalize()})
            else:
                resp = random.choice(Bot_verbs_with_noun).format(**{'noun': noun})
        else:
            resp = random.choice(Bot_verb_with_adjective).format(**{'adjective': adjective})
    return resp

# responses with noun 

Verbs_with_capial_plural_nouns_about_bot = [
    "My last theatrical release killed the {noun}",
    "Were you aware I was a cult figure within the {noun} genre?",
    "My film idea is a superhero {noun} franchise",
    "I really consider myself an expert on {noun}",
]

Bot_verbs_with_noun = [
    "Yeah  I know a lot about {noun}",
    "My fellow directors  always ask me about {noun}",
]

Bot_verb_with_adjective = [
    "I'm personally directing the {adjective} franchise",
    "I consider myself an expert in {adjective}",
]
# end

# Changes small i to capital
def capitalise_i(sentence):
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)

    #Parse the users input and respond
def respond(sentence):
    cleaned = capitalise_i(sentence)
    parsed = TextBlob(cleaned)

    # Finds the word classes of inputted sentence 
    pronoun, noun, adjective, verb = find_word_classes(parsed)

    # For when user is talking about the bot the bot will respond with the noun
    resp = check_for_comment_about_bot(pronoun, noun, adjective)

    # If user uses greeting word greet them back
    if not resp:
        resp = greeting_check(parsed)

    if not resp:
        # if bot doesnt understand the input it will respond from the doesnt understand list unless there is a pronoun
        if not pronoun:
            resp = random.choice(Response_for_when_bot_doesnt_understand)
        elif pronoun == 'I' and not verb:
            resp = random.choice(Bot_responding_about_itself)
        else:
            resp = answer_the_user(pronoun, noun, verb)

    # If none of above applies use doesnt understand response
    if not resp:
        resp = random.choice(Response_for_when_bot_doesnt_understand)


    return resp

def find_word_classes(parsed):
    # Given a parsed input from the user identify the best nouns, verbs, adjectives and pronouns 
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        verb = identify_verbs(sent)
        pronoun = identify_pronouns(sent)
        adjective = identify_adjectives(sent)
        noun = identify_nouns(sent)
    return pronoun, noun, adjective, verb


# Function to stop words from FILTER LIST being in the response
def filter_response(resp):

    for s in FILTER_WORDS:
        if word.lower().startswith(s):
                raise Filter_bad_words()

def main(saying):
    response = film_response(saying)
    print(response)
    return response


if __name__ == '__main__':
    if (len(sys.argv) > 0):
        saying = sys.argv[1]
    else:
        main(saying)

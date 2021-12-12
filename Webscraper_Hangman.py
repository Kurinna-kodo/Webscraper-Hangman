import requests
from bs4 import BeautifulSoup
import string
import os
import time
import timeout_decorator
from threading import Thread
from mylogger import getmylogger
import sys
import signal

#branch test 2


logger = getmylogger(__name__)



url = 'https://www.dictionary.com/e/word-of-the-day/'

def extract(url):

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    wordoftheday = soup.find_all('div', class_ = 'otd-item-headword')
    
    for item in wordoftheday:

        try:
            
            word = (item.find('div', class_ = 'otd-item-headword__word').text.strip())
            pronounciation = (item.find('div', class_ = 'otd-item-headword__pronunciation').text.strip())
            definition = (item.find('div', class_ = 'otd-item-headword__pos' ).text.strip())

            logger.debug(f"{word}{pronounciation}{definition}")
            return(word.upper(), pronounciation, definition.upper())
            
        except:
            logger.critical(f"Extraction did not work.")

        
        break


logger.info("Extract end without errors")

def display(word, guesses, bad_guesses):

    print('Attempted Letters: ' + ','.join(bad_guesses))
    print('\n')
    print(' '.join(guesses))
    print((len(word)) * "_ "  )


def hint():
    time.sleep(5)
    print('Hello')

@timeout_decorator.timeout(5)
def user_input():

    print('\n')
    print("You have 30 seconds to answer or else game over!\n")

    guess = '123'

    alphabet = string.ascii_uppercase

    while guess.upper() not in alphabet or len(guess.upper()) > 1:

        guess = input("Please pick a letter: A-Z: ").upper()
        
    return(guess)   
            
        
def counter(daily_word, good_guesses):

    count = 0
    tracker = []

    for x in good_guesses:

        for y in daily_word:
        
            count += 1
            
            if count > len(daily_word):
                count = 1 

            if x == y:
                tracker.append(count - 1)

    return(tracker)


def replace(guesses, tracker, word):

    while len(tracker) >= 1:

        guesses[tracker[-1]] = word[tracker[-1]]

        tracker.pop()

    return(guesses)


def win(guesses, daily_word):

    if ''.join(guesses) == daily_word:
        return True

    


def replay():

    replay = 'nonsense'

    while replay.startswith('Y') == False:

        replay = input('Would you like to try again? Yes or No?:  ').upper()
        os.system('clear')
    
        if replay.startswith('Y') == True:

            return True
        
        else:
            if replay.startswith('N') == True:

                break
        
        

        
def bad_guesses(good_guesses, all_guesses):

    library = []

    for x in all_guesses:

        if x not in good_guesses:

            library.append(x)
            
    return library

attempt = None

def check(hint):
    time.sleep(5)
    if attempt != None:
        return
    print(hint)


def main():
    
    game_play = 'namgnah'

    while game_play.startswith('Y') == False:

        word = extract(url)
        daily_word = word[0].upper()

        guesses = len(daily_word) * [" "]

        good_guesses = []
        all_guesses = []
        
        if len(daily_word) % 2 == 0:
            chances = int(len(daily_word)/2)

        else:

            chances = int((len(daily_word) - 1)/2)
        

        print(' ')
        print("Welcome to Hangman - Daily Word @ Dictionary.com Edition!")

        print("We've taken the word of the day at Dictionary.com for you to guess correctly.")
        print("Once you've guessed correctly.. we'll give you the pronounciation, part of speech and definition.")
        print("Come back daily for a new word!")

        print('\n')
        print(f"There are {len(daily_word)} letters in today's daily word.")
        print('\n')

        game_on = False

        game_play = input("Type yes if you are ready to play! ").upper()

        if game_play.startswith('Y'):

            os.system('clear')
            game_on = True
        
        else:
            os.system('clear')
        

       
        while game_on:
            
            print('\n')
            print(f"You have {chances} guesses remaining!\n")
            
            bad_guess = bad_guesses(good_guesses, all_guesses)
            display(daily_word,guesses,bad_guess)

            alphabet = string.ascii_uppercase

            try:

                attempt = user_input()
            except Exception:

                print("Game Over!")
                   
           
            if attempt in all_guesses:

                    os.system('clear')
                    print('\n')
                    print ("You've already used that letter. Please guess again.")

            elif attempt in daily_word:
                os.system('clear')
                print('\n')
                print("That's right. Good choice!")

                good_guesses.append(attempt)
                all_guesses.append(attempt)

                tracker = counter(daily_word, good_guesses)
                    
                replace(guesses,tracker,daily_word)


                if win(guesses,daily_word):

                        os.system('clear')
                        print('\n')
                        print("Congrats, you've guessed all the correct letters!!\n")
                        print("The word is " + word[0] + '\n') 
                        print("It's pronounced" + word[1]+ '\n')   
                        x = word[2]
                        print("The PART OF SPEECH is: " +  x.replace('\n','\n\nThe DEFINTION is... \n', 1))
                        print('\n')
                        
                        game_on = False
        

            else:

                os.system('clear')
                print('\n')
                
                chances -= 1
                all_guesses.append(attempt)

                if chances > 0:
                    
                    print("Sorry, that letter isn't in the word.. ")

                else:
                    
                    print("You are all out of attempts.")
                    print("Game Over!!")
                    print('\n')
                    game_on = False
                    
                    if replay():

                        os.system('clear')
                        game_play = 'namgnah'

                    
        
            

if __name__ == "__main__":
    main()

        
       

            
            
            
            











   






















































    








   


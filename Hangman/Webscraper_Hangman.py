import requests
from bs4 import BeautifulSoup
import string
import os
import time
from time import sleep
import multiprocessing
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s~%(levelname)s~%(message)s', filename='logfile.log', filemode='w' )

# Define extract() which uses requests library and BeautifulSoup to extract data from url https://www.dictionary.com/e/word-of-the-day/
def extract():
    
    url = 'https://www.dictionary.com/e/word-of-the-day/'
    # Request content from dictionary.com
    r = requests.get(url)
    #Parse data using html.parser
    soup = BeautifulSoup(r.content, 'html.parser')
    word_of_the_day = soup.find_all('div', class_ = 'otd-item-headword')
    status_code = r.status_code
    

    # Iterate through class 'otd-item-headword' to get daily word, pronounciation and definition
    for item in word_of_the_day:

        try:
            daily_word = (item.find('div', class_ = 'otd-item-headword__word').text.strip())
            pronounciation = (item.find('div', class_ = 'otd-item-headword__pronunciation').text.strip())
            definition = (item.find('div', class_ = 'otd-item-headword__pos' ).text.strip())
            logging.debug(f"{daily_word}{pronounciation}{definition}")
            return(daily_word.upper(), pronounciation, definition.upper())
        except:
            # If exception, log status code
            logging.critical(f"Extraction did not work. Status code is {status_code}")
            


# Define display() funtion which displays attempted letters, correct guesses and incorrect guesses
def display(daily_word, correct_letters, bad_guesses):
    # Display bad attempts for user reference
    print('Attempted Letters: ' + ','.join(bad_guesses))
    print('\n')
    # Display correctly guessed letters 
    print(' '.join(correct_letters))
    # Display a underscore for length of the daily word
    print((len(daily_word)) * "_ "  )

#Create countdown() to display live timer to user
def countdown(): 
    print('\n')
    t = 30  #Timer Duration
    while t+1: #Runs while timer > 0
        mins, secs = divmod(t, 60)
        # Format timer to illustrate minutes and seconds
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f'   You have {timer} seconds to answer or else game over!',end="\r")
        time.sleep(1)
        t -= 1 
    else:
        # Instruct user on how to continue once timer runs out
        os.system('clear')
        print('\n')
        print('Sorry.. You ran out of time!')
        print('\n')
        print('Press Enter to continue.') 
        logging.debug('Player ran out of time')

# Define user_input() to get users guess within a time limit
def user_input():
    user_guess = '123'
    alphabet = string.ascii_uppercase
    # Start internal timer
    start_time = time.time()

    while user_guess.upper() not in alphabet or len(user_guess.upper()) > 1:
        print('\n')
        user_guess = input("Guess a letter...").upper()
        if time.time() - start_time > 30:
            return None
        logging.debug(user_guess)
        return(user_guess)   

def hint(definition, daily_word, correct_letters, bad_guesses, chances):
    sleep(10) #Sleeps for 10 seconds before displaying 
    os.system('clear') #Clears so timer does not display twice
    print(f"You have {chances} guesses remaining!\n")
    
    def display(daily_word, correct_letters, bad_guesses):
        print('Attempted Letters: ' + ','.join(bad_guesses))
        print('\n')
        print(' '.join(correct_letters))
        print((len(daily_word)) * "_ "  )
    # Re-display after screen clear
    display(daily_word, correct_letters, bad_guesses)
    # Display hint
    print('\n')
    print("Here's a hint =] \n")
    print("The PART OF SPEECH is: " +  definition.replace('\n','\n\nThe DEFINTION is: \n', 1))
    print('\n')

# Define counter() to track correct guesses at the proper index in daily word    
def counter(daily_word, good_guesses):
    count = 0
    tracker = []
    # Iterate through each good guess
    for x in good_guesses:
        #Iterate through each letter in daily word
        for y in daily_word:
            # Add 1 to each index of daily word after each iteration
            count += 1
            # Check for multiple correct letters and reset count 
            if count > len(daily_word):
                count = 1 
            # If correct letter matches letter in daily word, append to tracker list
            if x == y:
                tracker.append(count - 1)
    logging.debug(tracker)

    return(tracker)

# Define replace() which replaces empty value with good guesses at the right index
def replace(correct_letters, tracker, daily_word):
    while len(tracker) >= 1:
        # Replaces empty value with corresponding letter in daily word at index
        correct_letters[tracker[-1]] = daily_word[tracker[-1]]
        #Removes last index used
        tracker.pop()
    return(correct_letters)

# Define win() which checks if ALL correctly guessed letters matches daily word
def win(correct_letters, daily_word):
    if ''.join(correct_letters) == daily_word:
        logging.info('Player has won game')
        return True

# Define replay() funtion to ask user if they want to try again
def replay():
    replay = 'nonsense'
    while replay.startswith('Y') == False:
        # Take input from user
        replay = input('Would you like to try again? Yes or No?:  ').upper()
        os.system('clear')

        # If user types 'Y', returns True
        if replay.startswith('Y') == True:
            #logger.info('Player has selected replay.')
            return True
        # If user types 'N', break
        else:
            if replay.startswith('N') == True:
                logging.info('Player has selected NOT to replay.')
                break
# Define bad_guesses() which tracks bad guesses       
def bad_guesses(good_guesses, all_guesses):
    library = []
    # For loop that iterates over all attempts and good attempts list. Added to library list if item is not found
    for x in all_guesses:
        if x not in good_guesses:
            library.append(x)
            
    return library

def main():
    game_play = 'namgnah'
    while game_play.startswith('Y') == False:

        daily_scrape = extract()
        daily_word = daily_scrape[0].upper()
        correct_letters = len(daily_word) * [" "]
        good_guesses = []
        all_guesses = []
        
        if len(daily_word) % 2 == 0:
            chances = int(len(daily_word)/2)
        else:
            chances = int((len(daily_word) - 1)/2)
        
        print(' ')
        print("Welcome to Hangman - Daily Word @ Dictionary.com Edition!")
        print("We've taken the word of the day at Dictionary.com for you to guess correctly.")
        print("Come back daily for a new word!")
        print('\n')
        print(f"There are {len(daily_word)} letters in today's daily word.")
        print('\n')

        game_on = False
        game_play = input("Type yes if you are ready to play! ").upper()

        if game_play.startswith('Y'):
            os.system('clear')
            game_on = True
            logging.info("Game start without errors.")
        else:
            os.system('clear')
        

        while game_on:
            print('\n')
            print(f"You have {chances} guesses remaining!\n")
            logging.debug(f"{chances} Chances remaining")
            bad_guess = bad_guesses(good_guesses, all_guesses)
            display(daily_word,correct_letters,bad_guess)
            defintion = daily_scrape[2]
            p1 = multiprocessing.Process(target = countdown)
            p2 = multiprocessing.Process(target=hint,args = [defintion,daily_word,correct_letters,bad_guess,chances])
            p1.start()
            p2.start()

            alphabet = string.ascii_uppercase
            attempt = user_input()

            p1.kill()
            p2.kill()

            if attempt in all_guesses:
                    os.system('clear')
                    print('\n')
                    print ("You've already used that letter. Please guess again.")
            
            elif attempt == None:
                print('\n')
                logging.debug('Player did not provide answer.')
                game_on = False
                    
                if replay():
                    os.system('clear')
                    game_play = 'namgnah'

            elif attempt in daily_word:
                os.system('clear')
                print('\n')
                print("That's right. Good choice!")

                good_guesses.append(attempt)
                all_guesses.append(attempt)
                tracker = counter(daily_word, good_guesses)
                replace(correct_letters,tracker,daily_word)
                logging.info('Player chose correct letter')

                if win(correct_letters,daily_word):
                        os.system('clear')
                        print('\n')
                        print("Congrats, you've guessed all the correct letters!!\n")
                        print("The word is " + daily_scrape[0] + '\n') 
                        print("It's pronounced" + daily_scrape[1]+ '\n')   
                        definition = daily_scrape[2]
                        print("The PART OF SPEECH is: " +  definition.replace('\n','\n\nThe DEFINTION is... \n', 1))
                        print('\n')
        
                        game_on = False
        
            else:
                os.system('clear')
                print('\n')
                chances -= 1
                all_guesses.append(attempt)
                logging.debug(all_guesses)

                if chances > 0:
                    print("Sorry, that letter isn't in the word.. ")

                else:
                    print(f"You have {chances} guesses remaining!\n")
                    bad_guess = bad_guesses(good_guesses, all_guesses)
                    display(daily_word,correct_letters,bad_guess)
                    print('\n')
                    print("You are all out of attempts. Game Over!!")
                    print('\n')
                    logging.info('Player ran out of attempt.')
                    game_on = False
                    
                    if replay():
                        logging.info('Player chose to replay.')
                        os.system('clear')
                        game_play = 'namgnah'

if __name__ == "__main__":
    main()

        

            
            
            
            











   






















































    








   


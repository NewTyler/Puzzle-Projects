import math
import numpy as np
import random
import sys
import json
import time
import reader
from termcolor import colored


#get_words
#inputs   : name - name of file to access
#outputs  : words - list of words from the file
#function : opens the associated file containing all words
#           the wordle could be
def get_words(name):

    wordsfile = open(name, 'r')
    words = wordsfile.readlines()
    wordsfile.close()
    return words


#get_user_fb
#inputs   : guess    - the current user guess
#outputs  : guessfb  - dict of the feedback received from the user
#function : asks the user to input the feedback they received from wordle
def get_user_fb(guess):
    guessfb = {}
    wordlen = 5

    #collect the performance of each letter according the wordle
    index = 0
    for index in range(wordlen):
        letter = input("If letter "+guess[index]+" is black (type 0), yellow (type 1), green (type 2): ")
        guessfb[index] = letter
    print(guessfb)
    return guessfb


#test_user_fb
#inputs   : guess       - the current guessed word
#         : guessfb     - the current feedback asssigned for the guessed word
#         : totalwords  - total number of words in the set
#         : words       - list of all possible wordle words
#         : wordprob    - dict containing the value of each word that could still be a possible solutions
#outputs  : wordprob    - updated dict of still possible solutions
#function : given the correct word, and the current guess feedback, iterates through all words
#           removing words that no longer are possible solutions. This updates the wordprob
#           dictionary
def test_user_fb(guess, guessfb, totalwords, words, wordprob):
    wordlen = 5

    i = 0
    for i in range(totalwords):
        currword = words[i][0:wordlen]
        # wordprob contains list of words that are still possible
        if currword not in wordprob:
            continue
        j = 0
        for j in range(wordlen):
            conditional = 1
            #if the current letter is black, remove applicable words
            if guessfb[j] == '0':
                #if the current letter matches the feedback letter, remove this word from wordprob
                if (guess[j] in currword):
                    wordprob.pop(currword)
                    break
            elif guessfb[j] == '2' and (guess[j] != currword[j]):
                wordprob.pop(currword)
                break
            elif guessfb[j] == '1' and ((guess[j] not in currword) or (guess[j] == currword[j])):
                wordprob.pop(currword)
                break
    return wordprob


#sim_fb
#inputs   : guess       - the current guessed word
#         : chosen_word - the randomly generateed solution for the wordle game
#         : totalwords  - total number of words in the wordle set
#         : words       - list of all possible wordle words
#         : wordprob    - dict containing the value of each word that could still be a possible solutions
#outputs  : wordprob    - updated dict of still possible solutions
#function : given the correct word, and the current guess, iterates through all words
#           removing words that no longer are possible solutions. This updates the wordprob
#           dictionary
def sim_fb(guess, chosen_word, totalwords, words, wordprob):
    wordlen = 5
    guessfb = [' ' for x in range(5)] 

    if (guess == chosen_word):
        return wordprob

    #determine the feedback of each letter
    for letter in range(wordlen):
        # if the letter matches the correct word, output this letter as green
        if guess[letter] == chosen_word[letter]:
            guessfb[letter] = '2'
        # if the letter is in the correct word, but wasnt in the right position, print as yellow
        elif guess[letter] in chosen_word:
            guessfb[letter] = '1'
        # if the letter is not in the word, output as white
        else :
            guessfb[letter] = '0'
    i = 0
    for i in range(totalwords):
        currword = words[i][0:wordlen]
        # wordprob contains list of words that are still possible
        if currword not in wordprob:
            continue
        j = 0
        for j in range(wordlen):
            conditional = 1
            #if the current letter is black, remove applicable words
            if guessfb[j] == '0':
                #if the current letter matches the feedback letter, remove this word from wordprob
                if (guess[j] in currword):
                    wordprob.pop(currword)
                    break
            elif guessfb[j] == '2' and (guess[j] != currword[j]):
                wordprob.pop(currword)
                break
            elif guessfb[j] == '1' and ((guess[j] not in currword) or (guess[j] == currword[j])):
                wordprob.pop(currword)
                break
    return wordprob


#game_fb
#inputs   : guess       : the current user guess
#         : chosenword  : the solution to the game
#outputs  : wordprob = updated dict of still possible solutions
#function : given the current guess and the solution to the wordle,
#           generates a color coordinated feedback string for the user
def game_fb(guess, chosen_word):
    wordlen = 5
    feedback = ''
    for letter in range (wordlen):
        
        # if the letter matches the correct word, output this letter as green
        if guess[letter] == chosen_word[letter]:
            feedback += colored(chosen_word[letter], 'green')

        # if the letter is in the correct word, but wasnt in the right position, print as yellow
        elif guess[letter] in chosen_word:
            feedback += colored(guess[letter], 'yellow')

        # if the letter is not in the word, output as white
        else :
            feedback += colored(guess[letter], 'white')
    return feedback


#wordle_assist
#inputs   : None
#outputs  : None
#function : suggests words to be played in the wordle,
#           calculates a value for all words according to the freqeuncy of each letter in its position
#           for the set of all words,
#           receives wordle feedback from the user to narrow down the possible words
#           suggests the word with the highest assigned value to guess
def wordle_assist():

    currword = ''
    wordlen = 5
    num_attempts = 6

    #load in all possible words for training

    words = get_words('words.txt')
    totalwords = len(words) 

    #obtain the initial probability of every word in the wordle set
    wordprob = train_data(words, totalwords)
    #obtain the highest valued first word to guess
    max_value = max(wordprob, key=wordprob.get)

    for attempt in range(num_attempts):
        #print the highest probability word to start off with
        print('The highest value word to start off with is: ' + max_value)
        print(wordprob[max_value])

        #receive the guess the user makes
        guess = input("Input your guess: ")

        #ask the user for the feedback observed from the wordle
        guessfb = get_user_fb(guess)
        
        #iterate through the list of all possible words removing words that clearly will not work
        wordprob = test_user_fb(guess, guessfb, totalwords, words, wordprob)

        #check if there is only one word possible, if so you have the correct answers
        if(len(wordprob) == 1):
            print('Congratulations, the solutions is: ' +str(wordprob))
            return
    
        #obtain the highest valued word to guess next
        max_value = max(wordprob, key=wordprob.get)



#play_wordle
#inputs   : None
#outputs  : None
#function : simulates the wordle guessing game
def play_wordle():
    currentguess = ['_', '_', '_', '_', '_']
    num_attempts = 6
    wordlen = 5
    
    #retreive list of possible words
    words = get_words('words.txt')
    totalwords = len(words)

    #randomly choose a word from the list of all words
    chosenindex = random.randint(0,totalwords-1)
    chosen_word = words[chosenindex][0:wordlen]

    print("Welcome to Today's Wordle!")

    #user gets 6 attempts to guess correctly
    for attempt in range(num_attempts):
        #get the users input, if input is not in list of all words, ask again
        
        guess = input(str(currentguess) + " -> ")
        while (guess+"\n") not in words:
            print('Improper input, try again')
            guess = input(str(currentguess) + " -> ")

        #user input has been collected, decide feedback to give
        
        feedback = game_fb(guess, chosen_word)

        print(feedback)
        if (guess) == chosen_word:
            print('Success! Won on attempt: '+ str(attempt+1))
            return
    print("You have run out of guesses, the correct word was: " +str(chosen_word))
    


#simulate_wordle
#inputs   : first_word - the word to be tested as the first guess
#         : num        - the number of simulated games to play
#outputs  : returns the success rate of that word as the first guess
#function : takes in a word to be tested as a first guess in wordle, and runs num
#         : simulations of the wordle game to test its efficacy
def simulate_wordle(first_word, num, words, wordprob):
    initial_wordprob = {}
    currword = ''
    wordlen = 5
    totalwords = len(words)

    #train initial dataset
    #count the number of occurences of each letter in each position
    initial_wordprob = wordprob

    num_attempts = np.zeros(num)
    num_fails = 0
    for sim in range(num):
        #print('Current Sim : '+str(sim))
        victory = False
        wordprob = initial_wordprob.copy()
        chosenindex = random.randint(0,totalwords-1)
        chosen_word = words[chosenindex][0:wordlen]

        #program gets 6 attempts to guess correctly
        for attempt in range(6):
            
            if (attempt == 0):
                guess = first_word

            elif (len(wordprob)>0):
                guess = min(wordprob, key=wordprob.get)

            else:
                print('something went wrong with with word '+str(chosen_word))
                print('current attempt: ' +str(attempt) + ' first word: ' +str(first_word))
                exit()
            #guessed the word correctly, set victory to True, store the num of attempts, break from loop
            if (guess == chosen_word):
                num_attempts[sim] = attempt
                victory = True
                break

            #update the wordprob dictionary with only words that are still possible solutions given the feedback
            wordprob = sim_fb(guess, chosen_word, totalwords, words, wordprob)
            

        #once done with all 6 attemots
        if (victory == False):
            num_fails += 1
            num_attempts[sim] = 6
        #if (sim>(num/2)) and (num_fails/sim >= 0.15):
        #    print('not worth: ' + str((1- (num_fails/sim))))
        #    return (1- (num_fails/sim)) 
            

    print('Average number of guesses until correct using ' + str(first_word)+' as the first guess: '+ str(sum(num_attempts) / len(num_attempts)))
    print('Success Rate: ' + str(1 - (num_fails/num)))
    print('Number of Fails: ' +str(num_fails))
    return (1 - (num_fails/num))


#train_data
#inputs   : words      - a list of evey word that can possible be a wordle solution
#         : totalwords - the number totalwords in the set of words
#outputs  : wordprob   - dict of every single word in the wordle set and its assigned value
#function : creates a dictionary that stores the frequency of a each letter occuring in each position
#           for every word in the wordle set. Then iterate through every word, adding the frequency of each
#           word occuring in each position to find the total 'value' of the word. The dictionary wordprob
#           will store this value for every word in the wordle set and return it
def train_data(words, totalwords):
    wordlen = 5
    letterdict = {}
    wordprob = {}

    #train initial dataset
    #count the number of occurences of each letter in each position
    for i in range(totalwords):
        currword = words[i][0:wordlen]
        for j in range(wordlen):
            if currword[j] in letterdict: #if letter already encountered, grab array and update it
                letterarray = letterdict[currword[j]]
                letterarray[j] += 1/(totalwords*wordlen)
                letterdict[currword[j]] = letterarray

            else:                                   #if first instance of letter, create an array for it
                letterarray = np.zeros(wordlen)
                letterarray[j] += 1/totalwords
                letterdict[currword[j]] = letterarray

    for i in range(totalwords): #calculate efficacy of each word
        currword = words[i][0:wordlen]
        wordprob[currword] = 0
        for j in range(wordlen):
            wordprob[currword] += math.log10(letterdict[currword[j]][j])
    return wordprob


#simulate_wordle
#inputs   : first_word - the word to be tested as the first guess
#         : num        - the number of simulated games to play
#outputs  : returns the success rate of that word as the first guess
#function : takes in a word to be tested as a first guess in wordle, and runs num
#         : simulations of the wordle game to test its efficacy
def word_menu():

    user = input("Press 1 if you would like to play the Wordle\nPress 2 if you would like to test a starting guess\nPress 3 if you would like to use Wordle word suggestion\n"+
                 "Press 4 if you would like to run the first word test\nPress 5 if you would like to see the top 10 optimal first guesses ")
    words = get_words('words.txt')
    totalwords = len(words)
    wordprob = train_data(words, totalwords)


    if user == ('1'):
        play_wordle()
    elif user == ('2'):
        guess = input('What word would you like to test? ')
        num = int(input('How many cycles would you like to test for? '))
        simulate_wordle(guess, num, words, wordprob)
    
    elif user ==('3'):
        wordle_assist()

    elif user == '4':
        
        success_dict = {}
        num  = int(input('How many simulations should be run per word? '))

        for test_first_word in range(totalwords):
            print('Testing word ' +str(words[test_first_word]) + ', number '+str(test_first_word) + ' out of ' +str(totalwords))
            start_time = time.time()
            success = simulate_wordle(words[test_first_word][0:5], num, words, wordprob)
            total_time = time.time() - start_time
            print('Time for execution: '+str(total_time))
            success_dict[words[test_first_word][0:5]] = success


        
        with open('resultV2.txt', 'w') as fp:
            json.dump(success_dict, fp)
    
    elif user == '5':

        results = json.load(open('resultV2.txt'))

        for i in range(10):
            best = max(results, key=results.get)
            print('Number '+str(i+1) + ' of the wordle set is: ' + str(best) + '. Its success rate is:  ' + str(results[best]))
            results.pop(best)


word_menu()
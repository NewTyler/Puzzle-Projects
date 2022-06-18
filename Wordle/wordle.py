

import reader
import math
import numpy as np
import naive_bayes as nb
import random
import sys
from termcolor import colored, cprint

def get_words(name):

    wordsfile = open(name, 'r')
    words = wordsfile.readlines()
    wordsfile.close()
    return words


def compute_wordle() :
    letterdict = {}
    wordprob = {}
    currword = ''
    wordlen = 5

    #load in all possible words for training

    words = get_words('words.txt')
    totalwords = len(words)


    #train dataset
    #count the number of occurences of each letter in each position
    for i in range(totalwords-1):
        currword = words[i][0:5]
        for j in range(wordlen):
            if currword[j] in letterdict.keys() : #if letter already encountered, grab array and update it
                letterarray = letterdict[currword[j]]
                letterarray[j] += 1/totalwords
                letterdict[currword[j]] = letterarray

            else:                                   #if first instance of letter, create an array for it
                letterarray = np.zeros(5)
                letterarray[j] += 1/totalwords
                letterdict[currword[j]] = letterarray

    for i in range(totalwords-1): #calculate efficacy of each word base on total
        currword = words[i][0:5]
        wordprob[currword] = 0
        for j in range(wordlen):
            wordprob[currword] += math.log10(letterdict[currword[j]][j])

    max_value = max(wordprob, key=wordprob.get)


    #done = 1
    for attempt in range(6):
        #receive user feedback from wordle
        print('The highest value word to start off with is: ' + max_value)
        print(wordprob[max_value])


        guess = input("Input your guess: ")

        print(guess)
        guessfb = {}

        index = 0
        for index in range(wordlen):
            letter = input("If letter "+guess[index]+" is black (type 0), yellow (type 1), green (type 2): ")
            guessfb[index] = letter
        print(guessfb)

        i = 0
        for i in range(totalwords-1):
            currword = words[i][0:5]
            if currword not in wordprob:
                continue
            #print(currword)
            j = 0
            for j in range(wordlen):
                conditional = 1

                if guessfb[j] == '0':
                    # print('break black')
                    if (guess[j] == currword[j]):
                        wordprob.pop(currword)
                        break

                    for check in range(wordlen):
                        if guessfb[check] == '2' and guess[check] == currword[j]: #dont pop
                            conditional = 0

                    if conditional == 1:
                        wordprob.pop(currword)

                    break

                elif guessfb[j] == '2' and (guess[j] != currword[j]):
                    #print('break green')
                    wordprob.pop(currword)
                    break

                elif guessfb[j] == '1' and ((guess[j] not in currword) or (guess[j] == currword[j])):
                    #print('break yellow')
                    wordprob.pop(currword)
                    break
                print('the word: '+currword+" is a possible guess")
                print(wordprob[currword])
                #else:
                    #print('success')

        #done = input('Did you win? Type 1 to continue, or 0 to stop: ')
        print(wordprob)
        max_value = max(wordprob, key=wordprob.get)
        #print(done)
        print(len(words))
        print(len(wordprob))



#simulates the wordle guessing game
def play_wordle() :
    currentguess = ['_', '_', '_', '_', '_']
    print(currentguess)

    words = get_words('words.txt')
    totalwords = len(words)

    chosenindex = random.randint(0,totalwords-1)
    chosen_word = words[chosenindex][0:5]
    print(chosen_word)
    print(words[chosenindex])

    print("Welcome to Today's Wordle!")

    for attempt in range(6):
        feedback = ''
        guess = input(str(currentguess) + " -> ")
        while (guess+"\n") not in words:
            print('Improper input, try again')
            guess = input(str(currentguess) + " -> ")
            #if (guess + "\n") in words:
            #    break

        for letter in range (5):
            if guess[letter] == chosen_word[letter]:
                feedback += colored(chosen_word[letter], 'green')

            elif guess[letter] in chosen_word:
                feedback += colored(guess[letter], 'yellow')

            else :
                feedback += colored(guess[letter], 'white')


        print(feedback)
        if (guess) == chosen_word:
            print('Success! Won on attempt: '+ str(attempt+1))
            break
        print("\033[1;22m This text is Bright Green  \n")








#compute_wordle()
play_wordle()
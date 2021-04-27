"""
Created on 10/26/2020

@author: Phillip Kang
"""
import random

def handleUserInputDebugMode():
    '''
    This function will prompt the user if they wish to play in debug mode.
    True is returned if the user enters the letter “d”, indicating debug mode
    was chosen; False is returned otherwise
    '''
    mode = input('Which mode do you want: (d)ebug or (p)lay: ')
    if mode == 'd':
        return True
    if mode == 'p':
        return False

def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard
    or (e)asy mode, then returns the corresponding number of misses
    allowed for the game.
    '''
    mode = input('Hard (8 misses) or Easy (8 misses) | (e or h?)> ')
    if mode == 'e':
        return 12
    if mode == 'h':
        return 8

def handleUserInputWordLength():
    '''
    This function will prompt the user if they wish to play in debug mode.
    '''
    length = input('How many letters in the word you will guess: ')
    word_length = int(length)
    return word_length

def createTemplate(currTemplate, letterGuess, word):
    '''
    This function will create a new template for the secret word that the
    user will see.
    '''
    for i in range(len(word)):
        if word[i] == letterGuess:
            currTemplate = currTemplate[:i] + letterGuess + currTemplate[i + 1:]
            word = word[:i] + '!' + word[i + 1:]
        else:
            pass
    return currTemplate

def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the
    information in the parameters.
    '''
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z']
    for i in range(len(alphabet)):
        if alphabet[i] in lettersGuessed:
            alphabet[i] = ' '
    space = ''.join(alphabet)
    misses_left = str(missesLeft)
    hangman = ' '.join(hangmanWord)
    line1 = r"letters not yet guessed: " + space + '\n'
    line1 += r"misses remaining = " + misses_left + '\n'
    line1 += hangman
    return line1
    pass

def getNewWordList(currTemplate, letterGuess, wordList, debug):
    '''
    This function constructs a dictionary of strings as the key to lists as the
    value.
    '''
    d = {}
    for i in wordList:
        key = createTemplate(currTemplate, letterGuess, i)
        if key in d:
            d[key].append(i)
        else:
            d[key] = [i]
    max_value = ('', [])
    for (k, v) in d.items():
        if len(v) > len(max_value[1]):
            max_value = (k, v)
        elif len(v) == len(max_value[1]):
            if k.count('_') > max_value[0].count('_'):
                max_value = (k, v)
            else:
                pass
    if debug == True:
        length_keys = len(d.keys())
        for (k, v) in sorted(d.items()):
            print(str(k) + ' : ' + str(len(v)))
        print('# keys = ' + str(length_keys))
    else:
        pass
    return max_value


def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks
    if it is a repeated letter.
    '''
    print(displayString)
    letter = input("letter> ")
    occur = 0
    while occur == 0:
        if letter not in lettersGuessed:
            occur += 1
            return letter
        else:
            print("you already guessed that")
            letter = input("letter> ")

def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    '''
    Takes the user's guess, the user's current progress on the word, and the
    number of misses left; updates the number of misses left and indicates
    whether the user missed.
    '''
    if guessedLetter in hangmanWord:
        return [missesLeft, True]
    else:
        missesLeft -= 1
        return [missesLeft, False]

def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message
    on whether or not the user won. True is returned if the user won the game.
    If the user lost the game, False is returned.
    '''
    debug = handleUserInputDebugMode()
    word_length = int(handleUserInputWordLength())
    misses = handleUserInputDifficulty()
    word_list = []
    wronganswers = 0
    file = open(filename)
    for line in file:
        word = str(line.strip())
        if len(word) == word_length:
            word_list.append(word)
    file.close()
    secretWord = word_list[random.randint(0, len(word_list) - 1)]
    currTemplate = '_' * word_length
    guessedletters = []
    missesleft = misses
    newTemplate = currTemplate
    new_list = word_list

    while missesleft > 0 and currTemplate != secretWord:
        currTemplate = newTemplate
        word_list = new_list
        print(createDisplayString(guessedletters, missesleft, currTemplate))
        if debug:
            print('(word is ' + str(secretWord) + ')')
            print('# possible words: ' + str(len(word_list)))
        guess = handleUserInputLetterGuess(guessedletters,
                                         createDisplayString(guessedletters,
                                                             missesleft,
                                                             currTemplate))
        answer = processUserGuessClever(guess, secretWord, missesleft)
        if not answer[1]:
            print('you missed: ' + guess + ' not in word')
        (newTemplate, new_list) = getNewWordList(currTemplate, guess,
                                                     word_list, debug)
        secretWord = new_list[random.randint(0, len(new_list) - 1)]
        answer = processUserGuessClever(guess, secretWord, missesleft)
        missesleft = answer[0]
        guessedletters.append(guess)

    if secretWord == currTemplate:
        print("you guessed word: " + secretWord)
        print('you made ' + str(len(guessedletters)) + ' guesses with ' + str(
            misses - missesleft) + ' misses')
        return True

    if wronganswers == 0:
        print("you're hung!!")
        print('word was ' + secretWord)
        print('you made ' + str(len(guessedletters)) + ' guesses with ' + str(
            misses) + ' misses')
        return False

if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame
    '''
    losses = 0
    wins = 0
    proceed = True
    while proceed == True:
        game = runGame('lowerwords.txt')
        if game == True:
            wins += 1
        else:
            losses += 1
        if input("Would you like to play again? | y or n> ") == 'n':
            print(
                "You won " + str(wins) + " game(s) " "and lost " + str(losses))
            proceed = False
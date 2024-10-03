import random # library required to randomly choose a secret word
from termcolor import colored

ALLOWED_GUESSES = 6

def get_secret_word() -> str:
	"""Returns a randomly generated secret word.
	Uses the list of words in the public domain retreived from:
	https://www-cs-faculty.stanford.edu/~knuth/sgb.html
	Requires a text file called words.txt.	
	"""
	with open('words.txt') as f:
		words = f.read().splitlines() 		
		word = random.choice(words)
	return word

def get_user_guess(secret_word: str) -> str:
	"""Returns the inputed user guess 
	after confirming it matches the secret word length.
	"""
	correct_input = False
	while not correct_input:
		user_word = str(input(f'Please guess a {len(secret_word)} letter word(your guess will be translated to full lowercase): ')).lower()
		if len(user_word) == len(secret_word) and user_word.isalpha(): #https://docs.python.org/3/library/stdtypes.html#string-methods
			correct_input = True
		else:
			print(f'Please input a {len(secret_word)} letter word, try again(spaces and non-alphabet characters are not allowed).')
	return user_word

def compare_words(secret_word: str, user_word: str) -> str:
	"""Compares the 2 words and returns a string of G, Y, or -.
	first it makes a list and checks for any greens, if its a green, appends it to the list.
	if not, appends a placeholder '__'. Afterwards, checks for yellows and checks for dupes.
	Then returns the string of all the G, Y, and -.
	"""
	matches = []
	green_index = 0
	yellow_index = 0
	result = ''
	while green_index < len(secret_word):
		if user_word[green_index] == secret_word[green_index]:
			matches.append(user_word[green_index] + 'G')
		else:
			matches.append('__')
		green_index += 1
	while yellow_index < len(secret_word):
		if matches[yellow_index][1] != 'G':
			if user_word[yellow_index] in secret_word:
				if ((matches.count(user_word[yellow_index] + 'G') + matches.count(user_word[yellow_index] + 'Y'))
				< secret_word.count(user_word[yellow_index])): #https://docs.python.org/3/library/stdtypes.html#string-methods
					matches[yellow_index] = user_word[yellow_index] + 'Y'
				else:
					matches[yellow_index] = user_word[yellow_index] + '-'
			else:
				matches[yellow_index] = user_word[yellow_index] + '-'
		yellow_index += 1
	for char in matches:
		result += char[1]
	return result

def color_guess(user_guess: str, matches: str) -> str:
	#takes in the users and the matches that colors the green, yellow and red letters.
	#then returns the word colored.
	colored_word = ''
	i = 0
	while i < len(user_guess):
		if matches[i] == 'G':
			colored_word += colored(user_guess[i], 'green')
		elif matches[i] == 'Y':
			colored_word += colored(user_guess[i], 'yellow')
		else:
			colored_word += colored(user_guess[i], 'red')
		i += 1
	return colored_word

def play_game(secret_word: str) -> bool:
	"""Plays the game for one session
	returns true for win or false for loss.
	"""
	guesses = 0
	win = False
	print(f'You will have {ALLOWED_GUESSES} guesses to guess the secret word.')
	while (win == False) and (guesses < ALLOWED_GUESSES):
		guesses += 1
		user_guess = (get_user_guess(secret_word))
		matches = (compare_words(secret_word, user_guess))
		colored_guess = color_guess(user_guess, matches)
		print(f'You guessed: {user_guess}.')
		if matches.count('G') == len(secret_word):
			win = True
		else:
			print('Not quite:')
			print(matches)
			print(colored_guess)
	return win

def main():
	wins = 0
	losses = 0
	playing = True
	while playing:
		secret_word = get_secret_word()
		win = play_game(secret_word)
		if win:
			wins += 1
			print('You win!')
		else:
			losses += 1
			print(f'Sorry you did not guess the word: {secret_word} in {ALLOWED_GUESSES} guesses.')
		print('Would you like to keep playing?')
		keep_playing = str(input('Type \"no\" to quit or anything else to keep playing: ')).lower()
		if keep_playing == 'no':
			playing = False
	print(f'Result - Wins: {wins} | Losses: {losses}')

if __name__ == '__main__':
    main()
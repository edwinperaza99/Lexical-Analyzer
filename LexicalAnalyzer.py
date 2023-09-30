# Used to exit program gracefully 
import time
import sys

# define separators, operators and reserved words
separator = [' ', '\n', '\t', ',', ';', '(', ')', '{', '}', '#']
operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
keyword = ['if', 'else', 'endif' ,'while', 'function', 'integer', 'bool', 'real', 'ret', 'put', 'get', 'true', 'false']
begin_comment = '[*'
end_comment = '*]'

# define array to store all the words that have been read
words = []

# define dictionary to store tokens
tokens = []

# Code to read the file and store its words in an array
def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            # here we store the current word read
            word = ""
            while True:
                char = file.read(1)
                if not char:
                    break  # End of file, we exit loop
                # check for comments
                if char == '[':
                    if word:
                        words.append(word)
                        word = ""
                    # check for correct opening comment
                    next_char = file.read(1)
                    if char + next_char == begin_comment:
                        words.append(char + next_char)
                    else:
                        # store single operator 
                        words.append(char)
                        # check if next character is a separator
                        if next_char in separator:
                            if next_char != ' ' and char != '\n' and char != '\t':
                                words.append(next_char)
                        else:    
                            word += next_char

                elif char in operators: # read operator
                    if word:
                        words.append(word)
                        word = ""
                    # check for double character operators
                    next_char = file.read(1)
                    # check for closing comment
                    if char + next_char == end_comment:
                        words.append(char + next_char)

                    elif char + next_char in operators:
                        words.append(char + next_char)
                    else:
                        # store single operator 
                        words.append(char)
                        # check if next character is a separator
                        if next_char in separator:
                            if next_char != ' ' and char != '\n' and char != '\t':
                                words.append(next_char)
                        # remove next if in case that we want to make this illegal
                        elif next_char in operators:
                            words.append(next_char)
                        else:    
                            word = next_char

                elif char in separator: # read separator
                    if word:
                        words.append(word)
                        word = ""
                    # in case that we dont want to store whitespaces
                    #remove "if" to keep whitespaces
                    if char != ' ' and char != '\n' and char != '\t':
                        words.append(char)
                else:
                    word += char
            if word:
                words.append(word)
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
    except PermissionError:
        print(f"You do not have permission to read the file: '{file_name}'.")
    except OSError as systemError:  
        print(f"An error occurred while reading the file: '{file_name}'. The error was: {systemError}")
    except Exception as errorMessage:
        print(f"An unexpected error occurred while reading the file: '{file_name}'. The error was: {str(errorMessage)}")

# finite state machine for real and integer
def FSMReal(lexeme):
    current_state = 1
    for char in lexeme:
        # manage initial state
        # we need this because we can't have a "." as the first character
        if current_state == 1:
            if char.isdigit():
                current_state = 2
            else:
                current_state = 5
        # manage state 2 aka integer before "."
        if current_state == 2:
            if char.isdigit():
                current_state = 2
            elif char == '.':
                current_state = 3
            else:
                current_state = 5
        # manage state 3 aka "."
        elif current_state == 3:
            if char.isdigit():
                current_state = 4
            else:
                current_state = 5
        # manage state 4 aka integer after "."
        elif current_state == 4:
            if char.isdigit():
                current_state = 4
            else:
                current_state = 5

    # if our final state is 4, then we have a real
    if current_state == 4:
        # store token and lexeme
        tokens.append({'token': 'real', 'lexeme': lexeme})
    # if our final state is 2, then we have an integer
    elif current_state == 2:
        tokens.append({'token': 'integer', 'lexeme': lexeme})
    # in case of failure
    else:
        tokens.append({'token': 'illegal', 'lexeme': lexeme})

# finite state machine for identifiers
def FSMIdentifier(identifier):
    current_state = 1
    if len(identifier) == 1:
        if identifier.isalpha():
            tokens.append({'token': 'identifier', 'lexeme': identifier})
    else:
        for char in identifier:
            # check if the first character is a letter
            if current_state == 1:
                if char.isalpha():
                    current_state = 2
                else:
                    current_state = 4
            # now we can accept digits and letters
            elif current_state == 2:
                if char.isalpha():
                    # we stay in the same state if letter
                    current_state = 2
                elif char.isdigit():
                    # we move to state 3 if digit
                    current_state = 3
                else:
                    current_state = 4
            # still accepting digits and letters
            elif current_state == 3:
                if char.isalpha():
                    # we go back to state 2 if letter
                    current_state = 2
                elif char.isdigit():
                    # we stay in the same state if digit
                    current_state = 3
                else:
                    current_state = 4
        # final state must be 2 because we need to end in a letter
        if current_state == 2:
            tokens.append({'token': 'identifier', 'lexeme': identifier})
        else:
            tokens.append({'token': 'illegal', 'lexeme': identifier})

# this is the main lexer function, it is in charge of identifying the tokens
def lexer(word):
    if word in keyword:
        tokens.append({'token': 'keyword', 'lexeme': word})
    elif word in operators:
        tokens.append({'token': 'operator', 'lexeme': word})
    elif word in separator:
        tokens.append({'token': 'separator', 'lexeme': word})
    # check if it is a real or an integer
    elif word[0].isdigit():
        FSMReal(word)
    # check if is in an identifier
    elif word[0].isalpha():
        FSMIdentifier(word)
    else:
        tokens.append({'token': 'illegal', 'lexeme': word})

# this functions removes comments from the code
def commentRemoval(words):
    # keep track if we are in a comment 
    comment = False
    # iterate through lexemes 
    for word in words:
        if word == begin_comment:
            comment = True
        elif comment == False:
            lexer(word)
        elif word == end_comment:
            comment = False

# this functions prints all the tokens to the main program console
def print_tokens(tokens):
    print("token\t\t\tlexeme")
    print("_________________________________\n")
    for token in tokens:
        if token['token'] == 'illegal' or token['token'] == 'keyword' or token['token'] == 'integer' or token['token'] == 'real':
            print(f"{token['token']}\t\t\t{token['lexeme']}")
        else:
            print(f"{token['token']}\t\t{token['lexeme']}")

# this function generates a file name for the tokens file
def file_name_generator(file_name):
    return 'output_' + file_name

# this function writes all the tokens and lexemes to a file
def write_tokens(tokens, file_name):
    try:
        output_file = file_name_generator(file_name)
        with open(output_file, 'w') as file:
            print(f"\nWriting tokens to file '{output_file}'...\n")
            file.write("token\t\t\tlexeme\n")
            file.write("_________________________________\n")
            for token in tokens:
                if token['token'] == 'illegal' or token['token'] == 'keyword' or token['token'] == 'integer' or token['token'] == 'real':
                    file.write(f"{token['token']}\t\t\t{token['lexeme']}\n")
                else:
                    file.write(f"{token['token']}\t\t{token['lexeme']}\n")
            print(f"Tokens written to file '{output_file}' successfully!\n")
    except FileNotFoundError:
        print(f"The file '{output_file}' was not found.")
    except PermissionError:
        print(f"You do not have permission to create the file: '{output_file}'.")
    except OSError as systemError:  
        print(f"An error occurred while creating the file: '{output_file}'. The error was: {systemError}")
    except Exception as errorMessage:
        print(f"An unexpected error occurred while creating the file: '{output_file}'. The error was: {str(errorMessage)}")

# Function to analyze a file
def analyze_file():
    while True:
        try:
            file_name = input("Please enter the name of the file you want to analyze (or 'q' to quit): ")
            if file_name == 'q':
                print("\nThank you for using our Lexical Analyzer!\n")
                print("Exiting program...")
                time.sleep(2)
                sys.exit(0) # Exit the loop and quit the program
            with open(file_name, 'r') as file:
                # The file exists, so continue with analysis
                print(f"\nAnalyzing file '{file_name}'...\n")
                words.clear()  # Clear the list of words from previous analyses
                tokens.clear()  # Clear the list of tokens from previous analyses
                read_file(file_name)
                commentRemoval(words)
                print_tokens(tokens)
                write_tokens(tokens, file_name)
                break
        except FileNotFoundError:
            print(f"The file '{file_name}' was not found. Please enter a valid file name.")
        except PermissionError:
            print(f"You do not have permission to read the file: '{file_name}'. Please enter a different file name.")
        except Exception as errorMessage:
            print(f"An unexpected error occurred: {str(errorMessage)} Please enter a different file name.")

# User interface
print("\nWelcome to our Lexical Analyzer!")

# call main function to analyze a file 
analyze_file()
# Main loop
while True:
    another_analysis = input("Do you want to analyze another file? (yes/no): ").strip().lower()
    if another_analysis == 'no' or another_analysis == 'n':
        print("\nThank you for using our Lexical Analyzer!\n")
        print("Exiting program...")
        time.sleep(2)
        sys.exit(0)  # Exit the program if the user does not want to analyze another file
    elif another_analysis == 'yes' or another_analysis == 'y':
        analyze_file()
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

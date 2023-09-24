# define separators, operators and reserved words
separator = [' ', '\n', '\t', ',', ';', '(', ')', '{', '}', '#', ':']
operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
reserved_words = ['if', 'else', 'endif' ,'while', 'function', 'integer', 'bool', 'real', 'ret', 'put', 'get', 'true', 'false']
begin_comment = '[*'
end_comment = '*]'

# define array to store all the words that have been read
words = []

# define dictionary to store tokens
tokens = []

# user interface
print("\nWelcome to our Lexical Analyzer")
file_name = input("Please enter the name of the file you want to analyze: ")
print(f"\nAnalyzing file '{file_name}'...\n")

# Code to read the file and store its words in an array
try:
    with open(file_name, 'r') as file:
        # here we store the current word read
        word = ""
        while True:
            char = file.read(1)
            if not char:
                break  # End of file, we exit loop
            if char in separator: # read separator
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

def FSMReal(lexeme):
    current_state = 1
    for char in lexeme:
        # manage initial state
        if current_state == 1:
            if char.isdigit():
                current_state = 2
            else:
                current_state = 5
        # manage state 2 aka integer before "."
        elif current_state == 2:
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


def FSMIdentifier(identifier):
    current_state = 1
    if len(identifier) == 1:
        if identifier.isalpha():
            tokens.append({'token': 'identifier', 'lexeme': identifier})
    else:
        for char in identifier:
            if current_state == 1:
                if char.isalpha():
                    current_state = 2
                else:
                    current_state = 4
            elif current_state == 2:
                if char.isalpha():
                    current_state = 2
                elif char.isdigit():
                    current_state = 3
                else:
                    current_state = 4
            elif current_state == 3:
                if char.isalpha():
                    current_state = 2
                elif char.isdigit():
                    current_state = 3
                else:
                    current_state = 4
        if current_state == 2:
            tokens.append({'token': 'identifier', 'lexeme': identifier})
        else:
            tokens.append({'token': 'illegal', 'lexeme': identifier})

def lexer(word):
    if word in reserved_words:
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


# call functions
commentRemoval(words)
print_tokens(tokens)
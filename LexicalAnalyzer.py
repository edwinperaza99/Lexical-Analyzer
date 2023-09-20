# define separators, operators and reserved words
separator = [' ', '\n', '\t', ',', ';', '(', ')', '{', '}', '#', ':']
operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
reserved_words = ['if', 'else', 'endif' ,'while', 'function', 'integer', 'bool', 'real', 'ret', 'put', 'get', 'true', 'false']
begin_comment = '[*'
end_comment = '*]'

# define array to store all the words that have been read
words = []

# user interface
print("\nWelcome to our Lexical Analyzer")
print("Please enter the name of the file you want to analyze:", end=" ")
file_name = input()
print(f"\nAnalyzing file '{file_name}'...\n")


# Code to read the file and store its words in an array
# file_name = 'test.txt'
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
        for word in words:
            print(word)
except FileNotFoundError:
    print(f"The file '{file_name}' was not found.")

print("\nJust testing initial setup\n")

def FSMReal(real):
    current_state = 1
    for char in real:
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
        print(f"real\t\t\t{real}")
    # if our final state is 2, then we have an integer
    elif current_state == 2:
        print(f"integer\t\t\t{real}")



def FSMIdentifier(identifier):
    print("identifier machine")
    current_state = 1
    if len(identifier) == 1:
        if identifier.isalpha():
            print(f"identifier\t\t{identifier}")
    else:
        for char in identifier:
            if current_state == 1:
                if char.isalpha():
                    current_state = 2
                else:
                    current_state = 5
            elif current_state == 2:
                if char.isalpha():
                    current_state = 2
                elif char.isdigit():
                    current_state = 2


def lexer(word):
    if word in reserved_words:
        print(f"keyword\t\t\t{word}")
    elif word in operators:
        print(f"operator\t\t{word}")
    elif word in separator:
        print(f"separator\t\t{word}")
    # check if it is a real or an integer
    elif word[0].isdigit():
        FSMReal(word)
    # check if is in an identifier
    # elif word[0].isalpha():
    #     FSMIdentifier(word)
    else:
        print(f"invalid\t\t\t{word}")

# keep track if we are in a comment 
comment = False

print("token\t\t\tlexeme")
print("______________________________")
for word in words:
    if word == begin_comment:
        comment = True
    elif comment == False:
        lexer(word)
    elif word == end_comment:
        comment = False

# define separators, operators and reserved words
separator = [' ', '\n', '\t', ',', ';', '(', ')', '{', '}', '#', ':']
operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
reserved_words = ['if', 'else', 'endif' ,'while', 'function', 'integer', 'bool', 'real', 'ret', 'put', 'get', 'true', 'false']

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

    # def FSMReal(real):

    # def FSMIdentifier(identifier):

def lexer(word):
    if word in reserved_words:
        print(f"keyword\t\t\t{word}")
    elif word in operators:
        print(f"operator\t\t{word}")
    elif word in separator:
        print(f"separator\t\t{word}")
    # check if it is a real or an integer
    # elif word[0].isdigit():
    #     FSMReal(word)
    # check if is in an identifier
    # elif word[0].isalpha():
    #     FSMIdentifier(word)
    else:
        print(f"invalid\t\t\t{word}")

print("token\t\t\tlexeme")
print("______________________________")
for word in words:
    lexer(word)

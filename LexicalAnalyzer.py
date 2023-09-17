# define separators, operators and reserved words
separator = [' ', '\n', '\t', ',', ';', '(', ')', '{', '}', '#', ':']
operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '==', '!=']
reserved_words = ['if', 'else', 'endif' ,'while', 'function', 'integer', 'bool', 'real', 'ret', 'put', 'get', 'true', 'false']

# define array to store all the words
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
            if char in separator:
                if word:
                    words.append(word)
                    word = ""
                # in case that we dont want to store whitespaces
                #remove "if" to keep whitespaces
                if char != ' ' and char != '\n' and char != '\t':
                    words.append(char)
                # words.append(char)
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
        print(f"{word} is a reserved word")
    elif word in operators:
        print(f"{word} is an operator")
    elif word in separator:
        print(f"{word} is a separator")
    # check if it is a real or an integer
    # elif word[0].isdigit():
    #     FSSMReal(word)
    # # check if is in an identifier
    # elif word[0].isalpha():
    #     FSMIdentifier(word)
    else:
        print(f"{word} is not a valid word for rat23f.")

print("token   lexeme")
for word in words:
    lexer(word)

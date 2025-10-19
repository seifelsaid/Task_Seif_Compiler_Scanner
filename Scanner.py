import re


keywords = {"int", "if", "return", "for", "char", "double", "while", "void", "float" ,"else"}


operators = re.compile(r"[+\-*/=<>!]+")
Special_Character = re.compile(r"[;,\(\)\{\}]")
identifier = re.compile(r"[a-zA-Z_]\w*")
numeric_constant = re.compile(r"\b\d+(\.\d+)?\b")
character_constant = re.compile(r"'(\\.|[^\\'])'")
whitespace = re.compile(r"[ \t]+")
newline = re.compile(r"\n")
single_line_comment = re.compile(r"//[^\n]*")
multi_line_comment = re.compile(r"/\*.*?\*/", re.DOTALL)  # ✅ Fixed

file_path = input("Enter the path of the C file you want to scan: ").strip()

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

tokens = []
position = 0

while position < len(code):
    match = None

    
    for token_type, pattern in [
        ('SINGLE_LINE_COMMENT', single_line_comment),
        ('MULTI_LINE_COMMENT', multi_line_comment),
        ('KEYWORD_OR_IDENTIFIER', identifier),
        ('NUMERIC_CONSTANT', numeric_constant),
        ('CHARACTER_CONSTANT', character_constant),
        ('OPERATOR', operators),
        ('Special_Character', Special_Character),
        ('NEWLINE', newline),
        ('WHITESPACE', whitespace)
    ]:
        match = pattern.match(code, position)
        if match:
            text = match.group()
            if token_type == 'KEYWORD_OR_IDENTIFIER':
                if text in keywords:
                    tokens.append(('KEYWORD', text))
                else:
                    tokens.append(('IDENTIFIER', text))
            elif token_type != 'WHITESPACE':  # Skip whitespace tokens
                tokens.append((token_type, text if token_type != 'NEWLINE' else '\\n'))
            break

    if match:
        position = match.end()
    else:
        position += 1

# Print tokens
for token in tokens:
    print(token)

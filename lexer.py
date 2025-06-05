import re  # Regular expressions modulu, metinden parca (token) bulmak icin

KEYWORDS = {"if", "else", "while", "for", "def", "return"}

TOKENS = [
    ("NUMBER",   r"\b\d+\b"),              
    ("ID",       r"\b[a-zA-Z_]\w*\b"), 
    ("LPAREN",   r"\("),                    
    ("RPAREN",   r"\)"),
    ("COMMA",    r","),                     
    ("OP",       r"==|!=|=|\+|\-|\*|\/|\<|\>"), 
    ("COLON",    r":"),                    
    ("COMMENT",  r"#.*"),                  
    ("SKIP",     r"[ \t]+"),              
    ("MISMATCH", r"."),                    
]

patternler = []
for isim, desen in TOKENS:
    patternler.append(f"(?P<{isim}>{desen})")

tum_desen = "|".join(patternler)
token_regex = re.compile(tum_desen)

class Token:
    def __init__(self, tur, deger):
        self.type = tur    
        self.value = deger 

    def __repr__(self):
        return f"{self.type}:{self.value}"

def tokenize(metin):
    tokens = []  
    for eslesen in token_regex.finditer(metin): 
        tur = eslesen.lastgroup   
        deger = eslesen.group()   

        if tur == "ID" and deger in KEYWORDS:
            tur = "KEYWORD"

        if tur == "SKIP":
            continue

        elif tur == "MISMATCH":
            raise RuntimeError(f"Geçersiz karakter: {deger}")

        tokens.append(Token(tur, deger))

    return tokens  

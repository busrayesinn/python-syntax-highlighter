from lexer import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Token listesi
        self.pos = 0  # Şu anki pozisyon

    def current_token(self):
        # Pozisyon geçerli mi, değilse EOF dön
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", "")

    def match(self, beklenen_tur):
        # Token türü beklenene uyuyorsa ilerle
        if self.current_token().type == beklenen_tur:
            self.pos += 1
            return True
        return False

    def parse(self):
        try:
            while self.pos < len(self.tokens):
                # Yorumları atla
                if self.current_token().type == "COMMENT":
                    self.pos += 1
                    continue

                if not self.statement():  # Her ifade doğru mu kontrol et
                    return False
            return True
        except:
            return False

    def statement(self):
        token = self.current_token()

        # if bloğu
        if token.type == "KEYWORD" and token.value == "if":
            self.match("KEYWORD")
            if not self.condition():
                return False
            if not self.match("COLON"):
                return False
            if not self.block():
                return False

            # else varsa kontrol et
            if self.current_token().type == "KEYWORD" and self.current_token().value == "else":
                self.match("KEYWORD")
                if not self.match("COLON"):
                    return False
                return self.block()
            return True

        elif token.type == "KEYWORD" and token.value == "def":
            self.match("KEYWORD")
            if not self.match("ID"):
                return False
            # Fonksiyon parametreleri varsa kontrol et
            if self.match("LPAREN"):
                while not self.match("RPAREN"):
                    if not self.match("ID"):
                        return False
                    if self.current_token().type == "COMMA":
                        self.match("COMMA")  # Virgül varsa atla
            if not self.match("COLON"):
                return False
            return self.block()

        # return ifadesi
        elif token.type == "KEYWORD" and token.value == "return":
            self.match("KEYWORD")
            return self.expression()

        # atama ifadesi
        elif self.match("ID"):
            if not self.match("OP"):
                return False
            return self.expression()

        return False


    def block(self):
        # En az bir statement olmalı
        if not self.statement():
            return False

        # Birden fazla satır varsa devam et
        while self.pos < len(self.tokens):
            if self.current_token().type == "COMMENT":
                self.pos += 1
                continue
            if not self.statement():
                break
        return True

    def condition(self):
        # koşul: ID OP NUMBER/ID şeklinde olmalı
        if not self.match("ID"):
            return False
        if not self.match("OP"):
            return False
        if not (self.match("NUMBER") or self.match("ID")):
            return False
        return True

    def expression(self):
        if self.match("LPAREN"):
            if not self.expression():
                return False
            if not self.match("RPAREN"):
                return False

            # Parantezden sonra operator varsa devam et
            while self.current_token().type == "OP":
                self.pos += 1
                if not self.expression():
                    return False
            return True

        elif self.match("ID") or self.match("NUMBER"):
            while self.current_token().type == "OP":
                self.pos += 1
                if not self.expression():
                    return False
            return True

        return False



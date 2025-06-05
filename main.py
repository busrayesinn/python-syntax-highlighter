import tkinter as tk
from lexer import tokenize
from parser import Parser

class KodVurgulamaUygulamasi:
    def __init__(self, pencere):
        self.pencere = pencere
        pencere.title("Gerçek Zamanlı Sözdizimi Vurgulayıcı")

        self.yazi_alani = tk.Text(pencere, wrap="word", font=("Courier", 14))
        self.yazi_alani.pack(expand=True, fill="both")

        self.renkler = {
            "KEYWORD": "blue",
            "ID": "black",
            "NUMBER": "darkorange",
            "OP": "red",
            "COMMENT": "green",
            "COLON": "purple"
        }

        for tur, renk in self.renkler.items():
            self.yazi_alani.tag_configure(tur, foreground=renk)

        self.sonuc_etiketi = tk.Label(pencere, text="", fg="red", font=("Arial", 12, "bold"))
        self.sonuc_etiketi.pack(anchor="w")

        self.yazi_alani.bind("<KeyRelease>", self.anlik_analiz_yap)

        # Deneme kodu
        deneme_kodu = """#deneme kodu
def hesapla(a, b):
    x = (a + b) * 3
    if x > 10:
        return x
    else:
        return (x + 5) """
        self.yazi_alani.insert("1.0", deneme_kodu)
        self.anlik_analiz_yap()

    def anlik_analiz_yap(self, event=None):
        icerik = self.yazi_alani.get("1.0", tk.END)
        self.temizle_etiketler()

        try:
            tokenler = tokenize(icerik)
            self.vurgula_tokenler(tokenler)

            parser = Parser(tokenler)
            if parser.parse():
                self.sonuc_etiketi.config(text="✅ Sözdizimi doğru", fg="green")
            else:
                self.sonuc_etiketi.config(text="❌ Sözdizimi hatası", fg="red")
        except Exception as e:
            self.sonuc_etiketi.config(text=f"Hata: {str(e)}", fg="red")

    def temizle_etiketler(self):
        for tur in self.renkler:
            self.yazi_alani.tag_remove(tur, "1.0", tk.END)

    def vurgula_tokenler(self, tokenler):
        # Arama pozisyonunu bastan baslatiyoruz her token icin
        for token in tokenler:
            start_index = "1.0"
            while True:
                pos = self.yazi_alani.search(token.value, start_index, tk.END, nocase=False)
                if not pos:
                    break
                end_pos = f"{pos}+{len(token.value)}c"
                self.yazi_alani.tag_add(token.type, pos, end_pos)
                start_index = end_pos

if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = KodVurgulamaUygulamasi(pencere)
    pencere.mainloop()

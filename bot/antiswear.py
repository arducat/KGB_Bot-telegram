# https://github.com/unixource/antiswear-ru v.1 main 

bpss = [
        ("ia", "я"),
        ("yo", "е"),
        ("ё", "е"),
        ("6", "б"),
        ("3", "з"),
        ("0", "о"),
        ("c", "с"),
        ("p", "р"),
        ("/\\", "л"),
        ]

prefixes = "хуе шлюх хуи хуй хую хуя пизд пезд блят бляд сук пидар пидор еб бзд пидр педр хул залуп спизд спизж пизж".split()
stdprefixes = "у ни а о вы до попере нев невъ за из изъ ис на недо надъ не о об объ от отъ по долба долбо под подъ пере пре пред предъ при про раз рас разъ съ со су через черес чрез черезъ вз взъ довы без бес".split()
short = "бля бл нах манда сучка мозгоеб мозгоебина".split()

all_symb = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")+list("abcdefghijklmnopqrstuvwxyz")+[" "]
for allow, _ in bpss:
    all_symb.append(allow)

for p in prefixes.copy():
    for stdp in stdprefixes:
        prefixes.append(stdp+p)

def replaceBypasses(word: str) -> str:
    for old, new in bpss:
        word = word.replace(old, new)
    before = ""
    output = ""
    for letter in word:
        if letter != before:
            output += letter
            before = letter
    return output

alphabet = "чCH цC шSH сS юYU яYA жZH аA бB вV гG дD еE зZ иI кK лL мM нN оO пP рR сS тT уU фF хH".lower().split()
def latin2cyrillic(word: str) -> str:
    for r in alphabet:
        word = word.replace(r[1:], r[0])
    return word

def pallBypasses(word: str) -> list[str]:
    output = []
    rb = replaceBypasses(word)
    lc = latin2cyrillic(word)
    output.append(rb)
    output.append(latin2cyrillic(rb))
    output.append(lc)
    output.append(replaceBypasses(lc))
    if __name__ == "__main__": 
        print("Обработано от byppass-ов:",output)
    return output

def swear(word: str) -> bool:
    for prefix in prefixes:
        if word.startswith(prefix) or (word in short):
            return True
    return False

def check(text: str) -> bool:
    text = text.lower()

    for s in text:
        if s not in all_symb:
            text = text.replace(s, "")

    # при условии, что матное слово будет в начале текста
    for fword in pallBypasses(text.replace(" ", "")[:10]):
        if swear(fword):
            return True

    for word in text.split():
        for word in pallBypasses(word):
            if swear(word):
                return True

    return False
        
from time import time
def test() -> None:
    print("-- ANTISWEAR --")
    print("Приставок в базе:",str(len(prefixes)))
    while True:
        inp = input("\nТекст: ")
        sttime = time() 
        print(">", check(inp))
        print("Проверено за:",str(time() - sttime))

if __name__ == "__main__":
    test()

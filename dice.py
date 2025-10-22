import secrets
import os

path_wordlist = os.path.join("words.txt")
words =[]

def load_words():
    global words

    if words:
        return words
    
    print(f"'{path_wordlist}' loading...")

    with open(path_wordlist, "r", encoding="utf-8") as f:
        clear_words = []
        
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()

            if parts:
                word = parts[-1]
                clear_words.append(word)

    words = clear_words
    print(f"{len(words)} words were successfully uploaded")
    return words

def passphrase(word_count = 6, reagent = "-"):
    words_ = load_words()
    
    if not words_:
        print("Error! word list empty.")
        return None
    
    words_chosen = []
    for i in range(word_count):
        safety_choice = secrets.choice(words_)
        chosen = words_chosen.append(safety_choice)

    return reagent.join(words_chosen)

    
if __name__ == "__main__":
    new_password = passphrase(word_count=6)
    print(new_password)




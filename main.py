from tokenizer.TextTokenizer import TextTokenizer

def main():
    text = 'My Name is Piyush 😂 ❤️ Khandelwal 😎. I\'m an software developer Hanji 💻 .';

    hindi_text = 'नमन अच्छा लड़का नहीं है';

    hindi_tokenizer_text(hindi_text);

    eng_tokenizer_text(text)

def eng_tokenizer_text(text):
    print(text);
    tokenizer = TextTokenizer(text, 'english');

    encodings = tokenizer.encode();
    print(encodings)

    real_text = tokenizer.decode(encodings);
    print(real_text);

def hindi_tokenizer_text(text):
    print(text);
    tokenizer = TextTokenizer(text, 'hindi');

    encodings = tokenizer.encode();
    print(encodings)

    real_text = tokenizer.decode(encodings);
    print(real_text);

    print(tokenizer.get_vocab_size())

if __name__ == "__main__":
    main()

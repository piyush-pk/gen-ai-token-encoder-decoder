# TextTokenizer

`TextTokenizer` is a Python class designed for tokenizing text, encoding tokens into unique numerical identifiers, decoding these identifiers back to text, and managing a persistent vocabulary stored in a JSON file. It provides a simple and efficient way to handle text tokenization and encoding for various natural language processing tasks.

## Features

- **Tokenization**: Splits input text into tokens based on spaces.
- **Encoding**: Converts tokens into unique integer IDs using a sequentially assigned identifier for each new token.
- **Decoding**: Converts integer IDs back to their corresponding tokens and reconstructs the original text.
- **Vocabulary Management**: Persists the vocabulary in a JSON file, allowing it to be reused and updated across sessions.

## Example

To use `TextTokenizer`, ensure you have the imported correctly.

- **Python 3.x**
- **`python-dotenv`** (for loading environment variables)

You can install `python-dotenv` using pip:

```bash
pip install python-dotenv

```

## Usage

```python
from tokenizer.TextTokenizer import TextTokenizer

def eng_tokenizer_text(text):
    print("English Text:", text)
    tokenizer = TextTokenizer(text, "english")
    encodings = tokenizer.encode()
    print("Encoded:", encodings)
    real_text = tokenizer.decode(encodings)
    print("Decoded:", real_text)

def hindi_tokenizer_text(text):
    print("Hindi Text:", text)
    tokenizer = TextTokenizer(text, "hindi")
    encodings = tokenizer.encode()
    print("Encoded:", encodings)
    real_text = tokenizer.decode(encodings)
    print("Decoded:", real_text)
    print("Vocabulary Size:", tokenizer.get_vocab_size())

# Example usage
english_text = "My Name is Piyush 😂 ❤️ Khandelwal 😎. I'm an software developer 💻 ."
hindi_text = "नमन अच्छा लड़का नहीं है"

eng_tokenizer_text(english_text)
hindi_tokenizer_text(hindi_text)

// output
English Text: My Name is Piyush 😂 ❤️ Khandelwal 😎. I'm an software developer 💻 .
Encoded: [4834, 49102214, 1828, 511834302817, 128514, 1008465039, 46171023131421321021, 12852675, 446822, 1023, 2824152932102714, 131431142124251427, 128187, 75]
Decoded: My Name is Piyush 😂 ❤️ Khandelwal 😎. I'm an software developer 💻 .

Hindi Text: नमन अच्छा लड़का नहीं है
Encoded: [404640, 526772762, 5033602162, 4057642, 5772]
Decoded: नमन अच्छा लड़का नहीं है
Vocabulary Size: 17
```

📚 How It Works
Tokenization: "My Name is" → ["My", "Name", "is"]

Encoding: Each token is assigned a unique ID → [101, 102, 103]

Decoding: Reverses encoding → [101, 102, 103] → "My Name is"

Persistence: Vocabulary is stored in a JSON file and updated as new tokens are encountered.


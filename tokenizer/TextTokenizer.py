import dotenv, os;
from .constants import get_all_printable_language_data;
from .utils import read_json_file, write_json_file

dotenv.load_dotenv();

class TextTokenizer:
    def __init__(self, text='', lang='english'):
        self.__FILE_PATH__ = os.getenv("VOCAB_FILE_PATH");

        self.__all_letters = get_all_printable_language_data(lang);

        self.__tokens = TextTokenizer.create_tokens(text);
        self.__vocab = self.__get_vocab_data();
        self.__decode_vocab = self.__get_decode_vocab();
        print(self.__all_letters)

    @staticmethod
    def create_tokens(text=''):
        return text.split(' ')

    def get_tokens(self):
        return self.__tokens
    
    def encode(self):
        return [ self.__get_encoded_value(token) for token in self.__tokens ];

    def __get_encoded_value(self, token = ''):
        if(token in self.__vocab):
            return self.__vocab[token];
        return self.__get_new_encoding(token);

    def __generate_encode_value(self, token):
        encoding = '';
        for c in token:
             if c in self.__all_letters:
                encoding  += str(self.__all_letters.index(c));
             else:
                encoding += str(ord(c))
        try:
            return int(encoding)
        except Exception:
            return 'UNKNOWN'

    def __save_new_encode_value(self, token, value):
        self.__vocab[token] = value;
        self.__decode_vocab[value] = token;
        write_json_file(self.__FILE_PATH__, self.__vocab);

    def __get_new_encoding(self, token):
        encoding = self.__generate_encode_value(token);
        self.__save_new_encode_value(token, encoding);
        return encoding;

    def __get_vocab_data(self) -> dict:
        return read_json_file(self.__FILE_PATH__);

    def __get_decode_vocab(self):
        return { value: key for key, value in self.__vocab.items() }

    def decode(self, encodings = []):
        return " ".join([self.__decode_vocab[encoding] for encoding in encodings]);

    def get_vocab_size(self):
        return len(self.__vocab.values())




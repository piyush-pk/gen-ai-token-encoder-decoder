import string;

__LANGUAGE_DATA__ = {
  'english': string.printable,
  'hindi': "".join(chr(x) for x in range(0x0900, 0x0980)),
  "russian": "".join(chr(x) for x in range(0x0400, 0x0500)),
  "chinese": "".join(chr(x) for x in range(0x4E00, 0x9FFF))
};

def get_all_printable_language_data(lang = 'english'):
  if lang != 'ALL' :
    return __LANGUAGE_DATA__[lang];

  language_data = '';
  for _, value in __LANGUAGE_DATA__.items():
    language_data += value;
  return language_data

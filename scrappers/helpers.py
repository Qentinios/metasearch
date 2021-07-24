def extract_number_from_string(text):
    return int(''.join(filter(str.isdecimal, text)))

import re
def search(word, text):
    pattern_1 = rf'{word.capitalize()}'
    pattern_2 = rf'{word.lower()}'
    result_1 = re.search(pattern_1, text)
    result_2 = re.search(pattern_2, text)
    if not result_1 is None or not result_2 is None:
        return 1
    else:
        return 0
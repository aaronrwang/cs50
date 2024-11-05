from cs50 import get_string


def main():
    phrase = get_string("Text: ")
    l = count_letters(phrase)
    w = count_words(phrase)
    s = count_sentences(phrase)
    L = l * 100 / w
    S = s * 100 / w
    i = 0.0588 * L - 0.296 * S - 15.8
    if i < 1:
        print("Before Grade 1")
    elif i > 16:
        print("Grade 16+")
    else:
        print("Grade " + str(round(i)))


def count_letters(phrase):
    count = 0
    for c in phrase:
        if c.isalpha():
            count += 1
    return count


def count_words(phrase):
    count = 1
    for c in phrase:
        if c == " ":
            count += 1
    return count


def count_sentences(phrase):
    count = 0
    for c in phrase:
        if c == "." or c == "?" or c == "!":
            count += 1
    return count


main()

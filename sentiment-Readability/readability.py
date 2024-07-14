# TODO
import cs50

paragraph = cs50.get_string("Text: ")


def main():
    letters = count_letters(len(paragraph))
    words = count_words(len(paragraph))
    sentences = count_sentences(len(paragraph))
    L = letters / words * 100
    S = sentences / words * 100
    y = (0.0588 * L) - (0.296 * S) - 15.8
    x = round(y)
    if x < 1:
        print("Before Grade 1")
    elif x < 16 and x >= 1:
        print(f"Grade {x}")
    else:
        print("Grade 16+")


def count_letters(length):
    count = 0
    for i in range(length):
        if paragraph[i].isalnum() == True:
            count += 1
    return count


def count_words(length):
    count = 1
    for i in range(length):
        if paragraph[i] == " ":
            count += 1
    return count


def count_sentences(length):
    count = 0
    for i in range(length):
        if paragraph[i] == "." or paragraph[i] == "!" or paragraph[i] == "?":
            count += 1
    return count


main()
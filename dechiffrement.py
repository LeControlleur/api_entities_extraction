from string import ascii_letters


def dechiffrement_cesar(messageCrypte, cle):
    result = ""
    for letter in messageCrypte:
        if letter in ascii_letters:
            ascii_num = ascii_letters.index(letter)
            # ascii_num = ord(letter)

            lowercase = True

            if ascii_num >= 26 : 
                lowercase = False

            ascii_num -= cle
            if not lowercase:
                ascii_num = ((ascii_num - 26) % 26) + 26
            else:
                ascii_num = ascii_num % 26

            result += ascii_letters[ascii_num]

        else:
            result += letter

    return result


if __name__ == "__main__":
    cle = ascii_letters.index('P')+1
    message = ""

    with open("files/testChiffre.md", "r") as f:
        for text in f.readlines():
            message += dechiffrement_cesar(text, cle)

    with open("files/test1.md", "w") as f:
        f.write(message)


    cle = ascii_letters.index('k')
    message = ""

    with open("files/testChiffre.md", "r") as f:
        for text in f.readlines():
            message += dechiffrement_cesar(text, cle)

    with open("files/test2.md", "w") as f:
        f.write(message)

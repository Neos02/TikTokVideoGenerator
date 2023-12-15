from better_profanity import profanity

profanity.load_censor_words()


def censor(text):
    original = text.split(' ')
    censored = profanity.censor(text).split(' ')

    for i in range(len(censored)):
        word = censored[i]

        if len(word) != 0 and len(word.replace('*', '')) == 0:
            try:
                censored[i] = censored[i].replace('*', original[i][0], 1)
            except IndexError:
                print(censored[i], original[i], 'error')

    return ' '.join(censored)

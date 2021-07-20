from PIL import Image
import os
import pytesseract
import pickle
import nltk

directory = "pics"


def stringify(dir):
    words = []
    for entry in os.scandir(dir):
        image = Image.open(entry.path)
        image = image.convert('L')
        text = pytesseract.image_to_string(image)
        words += [word for word in text.split()]
    return words

# print(stringify())


def tag():
    tagged = []
    words = stringify(directory)
    for i in words:
        tokenized = nltk.word_tokenize(i)
        # tagging creates a tuple of the (word, pos) -> ("I", "PRP")
        tagged += nltk.pos_tag(tokenized)
    return tagged


def tagged_dic():
    tokenized_dic = {}
    tagged = tag()
    for word, pos in tagged:
        if word == '‘':
            continue
        else:
            tokenized_dic[pos] = tokenized_dic.get(pos, []) + [word]
    return tokenized_dic


def pickles(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def unpickle(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    tag_dic = tagged_dic()
    # print(dir(pickle))
    pickles(tag_dic, "tagged")
    # print(unpickle("tagged"))

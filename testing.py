from PIL import Image
import os
import pytesseract
import pickle

directory = "pics"

def stringify(directory) -> lst:
    words = []
    for entry in os.scandir(directory):
        image = Image.open(entry.path)
        image = image.convert('L')
        text = pytesseract.image_to_string(image)
        words += [word for word in text.split()]
    return words

#print(stringify())

def tag() -> None:
    tagged = []
    words = stringify()
    for i in words:
        tokenized = nltk.word_tokenize(i)
        tagged += nltk.pos_tag(tokenized) #tagging creates a tuple of the (word, pos) -> ("I", "PRP")
    return tagged

def tagged_dic() -> dict:
    tokenized_dic = {}
    tagged = tag()
    for word, pos in tagged:
        if word == '‘':
            continue
        else:
            tokenized_dic[pos] = tokenized_dic.get(pos, []) + [word]
    return tokenized_dic


def pickle(obj, name) -> None:
    with open('/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def unpickle(name) -> dict:
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    tokenized_dic = tagged_dic()
    pickle(tokenized_dic, "dic")
    pic = unpickle()
    print(pic)
    print(type(pic))

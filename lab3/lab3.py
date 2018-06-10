import nltk
import re
from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def penn_to_wn(tag):
    if tag in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    elif tag in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ
    elif tag in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    return wn.NOUN


if __name__ == '__main__':
    client = MongoClient()
    posts = client.forum_inf.posts
    
    # normalization text from posts
    print('Converting text tokens to normal form...')
    texts = [post['text'] for post in posts.find().limit(1000)]
    result = []
    for text in texts:
        text = text.lower()
        tags = nltk.pos_tag(re.findall(r'[a-z]{2,}', text))
        for tag in tags:
            wn_tag = penn_to_wn(tag[1])
            normal = WordNetLemmatizer().lemmatize(tag[0], wn_tag)
            result.append(normal)

    print('Vectorization...')
    stop_words = [
        'youtube',
        'women',
        'anime',
    ]
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    result = vectorizer.fit_transform(result)
    print(result)

    km = KMeans()
    result = km.fit(result)
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(result.n_clusters):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()
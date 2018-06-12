import nltk
import re
import matplotlib
from pymongo import MongoClient
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud


matplotlib.use('Agg')


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
    print('Converting words to normal form...')
    texts = [post['text'] for post in posts.find().limit(1000)]
    all_words = []
    for text in texts:
        text = text.lower()
        tags = nltk.pos_tag(re.findall(r'[a-z]{2,}', text))
        for tag in tags:
            wn_tag = penn_to_wn(tag[1])
            normal = WordNetLemmatizer().lemmatize(tag[0], wn_tag)
            all_words.append(normal)

    print('Vectorization...')
    stop_words = [
        'youtube',
        'women',
        'anime',
    ]
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    vectors = vectorizer.fit_transform(all_words)
    print(vectors.shape)

    print('Creating clusters...')
    km = KMeans(n_clusters=4)
    result = km.fit(vectors)
    order_centroids = km.cluster_centers_.argsort()
    terms = vectorizer.get_feature_names()
    for i in range(result.n_clusters):
        print("Cluster {}:".format(i), end='')
        for indx in order_centroids[i, :15]:
            print(' {}'.format(terms[indx]), end='')
        print()
    print('Done')

    text = ' '.join(all_words)
    wc = WordCloud(background_color="white", max_words=2000)
    wc.generate(text)
    wc.to_file('cloud.png')

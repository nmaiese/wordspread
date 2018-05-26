# tutorial from https://nlpforhackers.io/topic-modeling/
import re
import os
import math
import pandas as pd
from functools import reduce
from nltk import word_tokenize
from nltk.corpus import stopwords
from gensim import models, corpora
from custom_stopword_tokens import custom_stopwords, specific_stop_words
from collections import Counter

OUT_FOLDER = 'data/'
if not os.path.exists(OUT_FOLDER):
    os.makedirs(OUT_FOLDER)


# Remove url from string
def remove_url_https(text):
    return re.sub(r"http\S+", "", text)


# Extract text from user tweets json file
def extract_dataset(json_file):
    dataset = pd.read_json(json_file)
    dataset['text'] = dataset['text'].apply(lambda x: remove_url_https(x))
    return dataset


def clean_text(text, stop_words):
    tokenized_text = word_tokenize(text.lower())
    cleaned_text = [t for t in tokenized_text if t not in stop_words and re.match('[a-zA-Z\-][a-zA-Z\-]{2,}', t)]
    return cleaned_text


def get_italian_stop_words(custom=True):
    stop_words = stopwords.words('italian')
    if custom:
        stop_words += custom_stopwords + specific_stop_words
    return list(set(stop_words))


# For gensim we need to tokenize the data and filter out stopwords
def tokenize(data, stop_words):
    tokenized_data = []
    for text in data:
        tokenized_data.append(clean_text(text, stop_words))
    return tokenized_data


def build_model(name, corpus, dictionary, model_name, num_topics=10,  num_doc=5):
    if model_name == 'lda':
        model = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
    elif model_name == 'lsi':
        model = models.LsiModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
    else:
        raise TypeError('%s invalid model. Must be "lda" or "lsi"' % model_name)
    model.save(OUT_FOLDER+name+'-'+model_name)
    print("=" * 20)
    print("Dataset: %s \nModel: %s" % (name, model_name))
    for idx in range(num_topics):
        print("Topic #%s:" % idx, model.print_topic(idx, num_doc))
    print()
    return model


def prepare_data(serie, stop_words):
    # Build a Dictionary - association word to numeric id
    dictionary = corpora.Dictionary(serie)
    # Transform the collection of texts to a numerical form
    corpus = [dictionary.doc2bow(text) for text in serie]
    return serie, dictionary, corpus


def get_token(idx, dictionary):
    return dictionary.id2token[idx]


def map_corpus(dataframe, dictionary, corpus):
    dataframe['index'] = dataframe.index
    return dataframe['index'].apply(lambda x: [(get_token(y[0], dictionary), y[1]) for y in corpus[x]])


def sum_corpus(data):
    return reduce(lambda x, y: Counter(dict(x)) + Counter(dict(y)), data['corpus'])


def concatenate_text(data):
    return reduce(lambda x, y: x + '.' + y, data)


def append_text(data):
    return reduce(lambda x, y: [x] + [y] if type(x) != list else x + [y], data)


def group_by_week(dataframe):
    dataframe['week'] = pd.to_datetime(dataframe['created_at'].dt.date) - pd.to_timedelta(7, unit='d')
    return dataframe.groupby('week').apply(sum_corpus).reset_index()


def group_by_month(dataframe):
    return dataframe.groupby([dataframe.created_at.dt.year.rename('year'), dataframe.created_at.dt.month.rename('month')])\
        .apply(sum_corpus).rename('text').reset_index()


def group_text_by_month(dataframe):
    return dataframe.groupby([dataframe.created_at.dt.year.rename('year'), dataframe.created_at.dt.month.rename('month')]) \
        .text.apply(concatenate_text).rename('grouped_text').reset_index()


def group_tweets_by_month(dataframe):
    return dataframe.groupby([dataframe.created_at.dt.year.rename('year'), dataframe.created_at.dt.month.rename('month')])[
        'text'].apply(lambda x: list(x)).rename('text').reset_index()


def concatenate_tweets_by_month(dataframe):
    dataframe['original_date'] = dataframe.created_at
    dataframe.created_at = dataframe.original_date.apply(lambda x: x.replace(day=1, hour=00, minute=00, second=00))
    merged = dataframe.groupby([dataframe.created_at])['text'].apply(lambda x: x.sum()).rename('text').reset_index()
    messages = dataframe.groupby([dataframe.created_at])['text'].apply(lambda x: list(x)).rename('messages').reset_index()
    messages['text_count'] = messages['messages'].apply(lambda x: len(x))
    return pd.merge(messages, merged, left_on=['created_at'], right_on=['created_at']).reset_index()


def concat_df(a, b):
    return pd.concat([a, b])


def return_empty_df():
    return pd.DataFrame()


# http://billchambers.me/tutorials/2014/12/21/tf-idf-explained-in-python.html
def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)


def sublinear_term_frequency(term, tokenized_document):
    return 1 + math.log(tokenized_document.count(term)) if tokenized_document.count(term) else 0


def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return 0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count)


def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values


def tfidf(tokenized_documents):
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

# TF-ID
#idf_values = text_process.inverse_document_frequencies(tokenized_data)
#tfidf_documents = text_process.tfidf(tokenized_data)

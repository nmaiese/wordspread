import text_process
import twitter_api
import topic_modeling as tm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
import json

stop_words = text_process.get_italian_stop_words()

# username = 'matteosalvinimi'
# username = 'matteorenzi'

# user_tweets = twitter_api.download_user_timeline(username, text_process.OUT_FOLDER)
# Group
# dataframe = text_process.concatenate_tweets_by_month(dataframe)

def generate_tf_id(username):

    raw = text_process.extract_dataset(text_process.OUT_FOLDER+username+'.json')
    raw['username'] = username
    dataframe = text_process.concatenate_tweets_by_month(raw)

    # Tokenize data

    dataframe['index'] = dataframe.index
    dataframe['token'] = dataframe['text'].apply(lambda text: text_process.clean_text(text, stop_words))
    # tokenized_data, dictionary, corpus = text_process.prepare_data(dataframe['token'], stop_words)
    # lda_model = text_process.build_model(username, corpus, dictionary, 'lda')
    # lsi_model = text_process.build_model(username, corpus, dictionary, 'lsi')
    # dataframe['corpus'] = text_process.map_corpus(dataframe, dictionary, corpus)

    # Group token by month
    data = text_process.group_text_by_month(dataframe)

    # https://markhneedham.com/blog/2015/02/15/pythonscikit-learn-calculating-tfidf-on-how-i-met-your-mother-transcripts/
    # Get TFIDF from grouped documents
    tf = TfidfVectorizer(analyzer='word', strip_accents='ascii', min_df=1, use_idf=True, stop_words=stop_words)
    # tfidf_matrix = tf.fit_transform(data.grouped_text)
    tfidf_matrix = tf.fit_transform(dataframe.text)
    cm = CountVectorizer(analyzer='word', strip_accents='ascii', min_df=0, stop_words=stop_words)
    # cm_matrix = cm.fit_transform(data.grouped_text)
    cm_matrix = cm.fit_transform(dataframe.text)
    feature_names = tf.get_feature_names()

    counter = tm.get_score(cm_matrix, feature_names, max_value=None)
    scores = tm.get_score(tfidf_matrix, feature_names, max_value=None)

    # data['score'] = [[{'text': key, 'value': value} for key, value in x.items()] for x in scores]
    # data['score'] = tm.merge(data['score'], counter, 'counter')
    # data['tweets'] = text_process.group_tweets_by_month(dataframe)['text']

    dataframe['score'] = [[{'text': key, 'value': value} for key, value in x.items()] for x in scores]
    dataframe['score'] = tm.merge(dataframe['score'], counter, 'counter')

    # Save
    dataframe.to_json(text_process .OUT_FOLDER+username+'-tfid.json', orient='records', date_format='iso')
    return dataframe, raw

# dataframe['text'] = dataframe['text'].apply(lambda text: ','.join(text_process.clean_text(text, stop_words)))
# tf = TfidfVectorizer(analyzer='word', use_idf=True, sublinear_tf=True, min_df=0, stop_words=stop_words)
# tfidf_matrix = tf.fit_transform(dataframe.text)
# feature_names = tf.get_feature_names()
#
# # Clustering Text
# km = KMeans(n_clusters=5, init='k-means++', max_iter=100, n_init=1)
# km_matrix = km.fit_transform(tfidf_matrix)
# clusters = km.labels_
# data['score'] = tm.get_score(tfidf_matrix, feature_names, max_value=None)

# TODO Best Keyword Ever


# usernames = ['luigidimaio', 'matteosalvinimi']
# total = text_process.return_empty_df()

# for username in usernames:
#     data, raw = generate_tf_id(username)
#     total = text_process.concat_df(total, raw)

# total.to_json(text_process.OUT_FOLDER+"-".join(usernames)+'-tfid.json', orient='records', date_format='iso')
# with open(text_process.OUT_FOLDER+"-".join(usernames)+'-tfid.json', 'r+') as f:
#     data = json.load(f)

# with open(text_process.OUT_FOLDER+"-".join(usernames)+'-tfid.json', 'w') as f:
#     data = {"data": data}
#     json.dump(data, f, indent=4)


# Facebook Parsers 

import pandas as pd 
import datetime

usernames = ['salvini', 'dimaio']
total = text_process.return_empty_df()

for username in usernames:
    df = pd.read_csv('data/'+username+'-fb.csv', delimiter='\t')
    df.post_message = df.post_message.fillna('')
    df = df[~df["post_message"].str.contains('shared')]
    df.by = username
    df.post_message = df.post_message.apply(str)
    df['created_at'] = df.post_published_unix.apply(lambda x: datetime.datetime.fromtimestamp(x))
    df = df.rename(columns={'post_message' : 'text'})
    df['text'] = df['text'].apply(lambda x: text_process.remove_url_https(str(x)))
    dataframe = text_process.concatenate_tweets_by_month(df)

    dataframe['index'] = dataframe.index
    dataframe['token'] = dataframe['text'].apply(lambda text: text_process.clean_text(text, stop_words))
    data = text_process.group_text_by_month(dataframe)
    tf = TfidfVectorizer(analyzer='word', strip_accents='ascii', min_df=1, use_idf=True, stop_words=stop_words)
    tfidf_matrix = tf.fit_transform(dataframe.text)
    cm = CountVectorizer(analyzer='word', strip_accents='ascii', min_df=0, stop_words=stop_words)
    cm_matrix = cm.fit_transform(dataframe.text)
    feature_names = tf.get_feature_names()

    counter = tm.get_score(cm_matrix, feature_names, max_value=None)
    scores = tm.get_score(tfidf_matrix, feature_names, max_value=None)

    dataframe['score'] = [[{'text': key, 'value': value} for key, value in x.items()] for x in scores]
    dataframe['score'] = tm.merge(dataframe['score'], counter, 'counter')

    # Save
    dataframe.to_json(text_process .OUT_FOLDER+username+'-tfid-fb.json', orient='records', date_format='iso')
    total = text_process.concat_df(total, df)

total.to_json(text_process.OUT_FOLDER+"-".join(usernames)+'-tfid-fb.json', orient='records', date_format='iso')
with open(text_process.OUT_FOLDER+"-".join(usernames)+'-tfid-fb.json', 'r+') as f:
    data = json.load(f)

with open(text_process.OUT_FOLDER+"-".join(usernames)+'-tfid-fb.json', 'w') as f:
    data = {"data": data}
    json.dump(data, f, indent=4)



def get_score(tfidf_matrix, feature_names, max_value=20):
    dense = tfidf_matrix.todense()
    result = []
    for i, row in enumerate(dense):
        month_words = row.tolist()[0]
        word_scores = [pair for pair in zip(range(0, len(month_words)), month_words) if pair[1] > 0]
        sorted_words_scores = sorted(word_scores, key=lambda t: t[1] * -1)
        words = {}
        for word, score in [(feature_names[word_id], score) for (word_id, score) in sorted_words_scores ][:max_value]:
            words[word] = score
        result.append(words)
    return result


def merge(data, values, value_name='value'):
    for i, row in data.iteritems():
        for word in row:
            if word['text'] in values[i]:
                    word[value_name] = values[i][word['text']]
            else:
                print('%s non trovato in %s' % (word['text'], value_name[i]))
    return data




import re, nltk, bs4
import pandas as pd
import numpy as np
from numpy.linalg import norm
import scipy as sp
from scipy.sparse import csr_matrix as csr
from string import punctuation
from nltk.corpus import stopwords
from collections import defaultdict

def tf(tweets):
    nltk.download('stopwords')
    punc = list(punctuation)
    stop_words = set(stopwords.words("arabic") + stopwords.words("english"))
    data = [tweets[x] for x in tweets]
    n = len(data) // 2
    maximum_per_document = defaultdict(int)
    number_docs_containing_term = defaultdict(int)

    def bow_count(sentences):
        new_sentence = ''
        sentences = re.sub(r'<\s*br\s*\/s*>', '', sentences)
        sentences = re.sub(r'\n>', ' ', sentences)
        sentences = re.sub(r'\s+', ' ', sentences)
        sentences = re.sub(r'\.+\s*', '.', sentences)

        for el in sentences:
            if el.isspace() or el.isalpha() or el == '.':
                new_sentence += el.lower()
        new_sentences = new_sentence.split('.')
        new_sentences = [set(e for e in el.split() if e not in stop_words) for el in new_sentence.split('.')]
        temp_set = set()
        temp_count = defaultdict(int)
        for el in new_sentences:
            for l in el:

                temp_count[l] += 1
                temp_set.add(l)

        doc_max_term_count = [v for k,v in sorted(temp_count.items(), key= lambda x : x[1], reverse=True)][0]

        for term in temp_set:
            number_docs_containing_term[term] += 1

        return temp_count, doc_max_term_count 

    docs = []
    i = 0
    for doc in data:
        counted_terms, m = bow_count(doc)
        maximum_per_document[i] = m
        docs.append(counted_terms)
        i += 1


    def get_tf_idf(w,doc_index):
        tf_idf = {}
        tf = {}

        for k,v in w.items():
            tf[k] = v / maximum_per_document[doc_index]
            ni = number_docs_containing_term[k]
            from math import log
            idf = log(n / ni)
            tf_idf[k] = tf[k] * idf

        return tf_idf

    result = []
    words_vector = set()
    for ind, words in enumerate(docs):
        ranked_words = get_tf_idf(words, ind)
        top_n = {k:v for k,v in sorted(ranked_words.items(), key=lambda x: (-x[1]) ) }
        result.append(top_n)
        top_set = set([el for el in top_n.keys()])
        words_vector |= top_set

    all_word_vector = np.zeros(len(words_vector))
    similarity_to_stack = []
    def similarity_vector(words):
        doc_vec = all_word_vector.copy()

        for i,word in enumerate(words_vector):
            if word in words:
                doc_vec[i] = 1

        doc_vec_norm = np.linalg.norm(doc_vec)
        doc_vec /= doc_vec_norm

        return doc_vec

    for progress,r in enumerate(result):
        similarity_to_stack.append(similarity_vector(list(r.keys())))

    m = csr(np.vstack(similarity_to_stack))
    ref = m.dot(m.T).toarray()
    return ref, data
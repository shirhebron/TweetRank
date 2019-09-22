from collections import OrderedDict
import numpy as np
import read_input
import spacy
import nltk
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en_core_web_sm')
from nltk.tokenize import TweetTokenizer



def word_count(string):
    tokens = string.split()
    n_tokens = len(tokens)
    return n_tokens

def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

def TweetWordRanker(word_counter, word_ranks):
    sumRanks=0
    for rank in word_ranks.values():
        sumRanks=sumRanks+rank

    return (sumRanks/word_counter)


class TextRank4Keyword():
    ## TextRank code WRITTEN BY Xu LIANG
    """Extract keywords from text"""

    def __init__(self):
        self.d = 0.85  # damping coefficient, usually is .85
        self.min_diff = 1e-5  # convergence threshold
        self.steps = 10  # iteration steps
        self.node_weight = None  # save keywords and its weight

    def set_stopwords(self, stopwords):
        """Set stop words"""
        for word in STOP_WORDS.union(set(stopwords)):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True

    def sentence_segment(self, doc, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for sent in doc.sents:
            selected_words = []
            for token in sent:
                # Store words only with cadidate POS tag
                if token.pos_ in candidate_pos and token.is_stop is False:
                    if lower is True:
                        selected_words.append(token.text.lower())
                    else:
                        selected_words.append(token.text)
            sentences.append(selected_words)
        return sentences

    def get_vocab(self, sentences):
        """Get all tokens"""
        vocab = OrderedDict()
        i = 0
        for sentence in sentences:
            for word in sentence:
                if word not in vocab:
                    vocab[word] = i
                    i += 1
        return vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i + 1, i + window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, vocab, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = vocab[word1], vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm != 0)  # this is ignore the 0 element in norm

        return g_norm

    def get_keywords(self, number=20):
        """Print top number keywords"""
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        for i, (key, value) in enumerate(node_weight.items()):
            print(key + ' - ' + str(value))
            if i > number:
                break

    def analyze(self, text,
                candidate_pos=['NOUN', 'PROPN','VERB','ADJ'],
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""

        # Set stop words
        self.set_stopwords(stopwords)

        # Pare text by spaCy
        doc = nlp(text)

        # Filter sentences
        sentences = self.sentence_segment(doc, candidate_pos, lower)  # list of list of words

        # Build vocabulary
        vocab = self.get_vocab(sentences)

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(vocab, token_pairs)

        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1 - self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr)) < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight






if __name__ == "__main__":
    main_dict = {}  ## just dict from csv - key: uniqe id, val : [user name, text , num retweet+num likes]
    user_value = {}  ## key: user name, val: user value
    tweet_text = {}  ## key : uniqe id , val: full text of the tweet
    final_tweet = {}  ## key: uniqe id, val : [text , user value , user name]
    final_tweet, tweet_text = read_input.read_write('input3_img.csv',main_dict , user_value , tweet_text, final_tweet)
    text2 = ''
    for i in tweet_text.items():
        sen = i[1].lower()
        text2 += sen +' '

    text=text2

    wordCounter=word_count(text2)
    tr4w = TextRank4Keyword()
    tr4w.analyze(text, candidate_pos=['NOUN', 'PROPN','VERB','ADJ'], window_size=4, lower=False)
    #tr4w.get_keywords(100)
    key_word_ranks = tr4w.node_weight

    TweetAverageWordRank= TweetWordRanker(wordCounter, key_word_ranks)
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    sum_user = 0
    sum_text = 0


    for i in tweet_text.items():
        tweet_val = 0
        words = i[1].split()
        for word in words:
            word=word.lower()
            wordlist = tknzr.tokenize(word)
            g = []
            for ii in wordlist:
                if ii.isalpha() or '#' in ii or '@' in ii:
                    g.append(ii)
            for w in g:
                if w in key_word_ranks:
                    tweet_val+=key_word_ranks[w]
            tweet_val = tweet_val / len(w)
        final_tweet[i[0]].append(tweet_val)
    #print("tweet rank =",TweetAverageWordRank)

    for hyper in range(0,21):
        change=hyper*0.05
        text_hyper = change
        user_hyper = 1-text_hyper

        rank_tweet=list()
        bb=[]
        for num in final_tweet.items():
            sum_text+=num[1][3]
            sum_user+=num[1][2]

        for tw in final_tweet.items():
            text_val = tw[1][3] / sum_text
            user_val = tw[1][2] / sum_user
            new_value = (text_hyper * text_val) + (user_hyper * user_val)
            temp = (tw[0],new_value)
            rank_tweet.append(temp)
        bb=sorted(rank_tweet, key=lambda x: x[1] , reverse=True)

        topten={}
        count=0
        for co in bb:
            temp1=[co[0],final_tweet[co[0]][1],final_tweet[co[0]][0]]
            topten[count] = temp1
            if count == 10:
                break
            else:
                count+=1

        print("text hyper",text_hyper)
        for pr in topten.items():
            print(pr)

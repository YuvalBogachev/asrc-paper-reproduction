from collections import defaultdict, Counter
from math import log


def extract_keys(key):
    """
    extract_keys take the key from a data structure from data.py and breaks it down to individual keys
    :param key: the key to break down
    :return: a collection of keys (query, round, author) (int)
    """

    if len(key) <= 3:
        return -1, int(key), -1
    else:
        return int(key.split('-')[1]), int(key.split('-')[0]), int(key.split('-')[2])


# TODO: Implement a function to remove stopwords for a stream/sentence
def remove_stopwords():
    pass


# TODO: Finish implmenting all the features for the vectorize function
def vectorize_documents(qry, docs):

    """
    vectorize_documents turn a corpus of documents and a matching query into feature vectors
    :param qry: the query matching the documents
    :type qry: str
    :param docs: a corpus of documents
    :type docs: dict
    :return: an array of feature vectors
    """

    def query_term_features(document, query):

        """
        query_term_features produces the query term (covered and not covered) feature for the document and the
        respective query
        :param document: the document created for the query
        :type document: str
        :param query: the query matching the document
        :type query: str
        :return: an array of features (int)
        """

        query_terms = set(query.split())
        occurrence_counter = 0

        for word in document.split():
            if word in query_terms:
                occurrence_counter += 1

        return [occurrence_counter, occurrence_counter / len(document.split())]

    def stream_length_feature(document):

        """
        stream_length_feature produces the stream length (number of terms) feature of the document
        :param document: a document from which we extract stream length
        :type document: str
        :return: length of stream (list of int)
        """

        return [len(document.split())]

    def idf_feature(query, documents):

        """
        idf_features produces the (feature of) average idf of all terms that appear in the query
        :param query: the query
        :param documents: a corpus of documents to calculate the average idf over
        :type documents: dict
        :return: the average idf (int)
        """

        query_terms = query.split()
        query_term_list = []
        average_idf = 0

        for document in documents:
            # Calculate the document frequency of each query term
            set_of_query_terms = set()
            for term in documents[document].split():
                if term in query_terms:
                    set_of_query_terms.add(term)
            query_term_list += list(set_of_query_terms)
        query_term_count = dict(Counter(query_term_list))

        # Calculate the average idf
        for term in query_term_count:
            average_idf += ((log(len(documents) / query_term_count[term])) / (len(set(query_terms))))
        # For terms unseen in the corpus
        for term in query_terms:
            if term not in query_term_count:
                average_idf += ((log((len(documents)) + 1 / 1)) / len(set(query_terms)))
        return average_idf

    # TODO: Implmenet features 21-70 of Microsoft's learning to rank datasets
    def tf_features(document):
        pass

    # TODO: Implement features 71-95 of Microsoft's learning to rank datasets
    def tf_idf_features(documents):
        pass

    # TODO: Implement features 110,120,125 of Microsoft's learning to rank datasets
    def lm_features(query, document):
        pass

        def create_unigram_lm(d):

            """
            create_unigram_lm creates an unigram language model from the document
            :param d: the document to base the language model on
            :type d: str
            :return: language model dictionary, words and their probabilities
            """

            lm = defaultdict(float)
            lm_size = len(d.split())

            for word in d.split():
                lm[word] += (1 / lm_size)

            return lm

        def create_collection_lm(ds):

            """
            create_collection_lm creates a unigram collection langauge model using micro averaging
            :param ds: the collection of documents
            :type
            :return: language model dictionary, words and their probabilities
            """

            lm = defaultdict(float)

            for d in ds:
                for term in ds[d]:
                    lm[term] += ((1 / len(ds)) * (1 / len(d)))

            return lm


        def create_dirichlet_lm(d, d_unigram_lm, mu):
            """
            create_dirichlet_lm creates a dirichlet smoothed language model from the document and corpus
            :param d: the document to base the language model on
            :type d: str
            :param d_unigram_lm: the langauge model of the corpus (collection language model)
            :type d_unigram_lm: dict
            :param mu: the smoothing free parameter
            :type mu: int
            :return: language model dictionary, words and their probabilities
            """

            lm = {}
            unigram_lm = create_unigram_lm(d)

            for word in unigram_lm:
                lm[word] = (unigram_lm[word] + mu * d_unigram_lm[word]) / (len(d.split()) + mu)

            return lm

        def create_jm_lm(d, d_unigram_lm, beta):

            """
            create_jm_lm creates a Jelinek-Mercer smoothed language model from the document and corpus
            :param d: the document to base the language model on
            :type d: str
            :param d_unigram_lm: the langauge model of the corpus (collection language model)
            :type d_unigram_lm: dict
            :param beta: the smoothing free parameter
            :type beta: int
            :return: language model dictionary, words and their probabilities
            """

            lm = {}
            unigram_lm = create_unigram_lm(document)

            for word in unigram_lm:
                lm[word] = (beta * unigram_lm[word]) + ((1 - beta) * d_unigram_lm[word])

            return lm

        def n_cross_entropy(dist1, dist2):

            """
            n_cross_entropy calculates the negative cross entropy between to distributions
            :param dist1: a distribution to calculate negative cross entropy for
            :type dist1: dict
            :param dist2: a distribution to calculate negative cross entropy for
            :type dist2: dict
            :return: int of negative cross entropy
            """

            # Cross entropy can only be preformed when the two distributions have the same domain
            common_values = [item for item in dist1 if item in dist2]

            ce = 0
            for value in common_values:
                ce += ((1 / len(common_values)) * (dist1[value] * log(dist2[value])))

            return ce

        pass

    # TODO: Implement the stopword features of the model
    def stopwords_features():

        # TODO: Implement a function to get the top 100 stopwords from ClueWeb09
        def get_top100_stopwords():
            pass

        # TODO: Implement the stopwords to non-stopwords ratio feature
        def stopwords_ratio():
            pass

        # TODO: Implement the percentage of stopwords feature
        def stopwords_percentage():
            pass

        pass

    # TODO: Implement the entropy feature
    def entoropy_feature():
        pass

    # TODO: Fill missing function arguments
    def create_feature_vector(document, documents, query):
        doc_vector = []
        doc_vector += query_term_features(document, query)
        doc_vector += stream_length_feature(document)
        doc_vector += idf_feature(documents)
        doc_vector += tf_features(document)
        doc_vector += tf_idf_features()
        doc_vector += lm_features()
        doc_vector += stopwords_features()
        doc_vector += entoropy_feature()

        return doc_vector

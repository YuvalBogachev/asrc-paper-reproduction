import constants
from krovetzstemmer import Stemmer


# TODO: Implement a function to read the ClueWeb09 documents
def get_clueweb09_documents():
    pass


def get_competition_documents():

    """
    get_competition_documents reads the competition documents file are return a document data structure (dict)
    :return: dict of documents
    """

    documents = {}
    stemmer = Stemmer()

    # UTF8 is required to properly read the file
    with open(constants.DOCUMENTS_FILE, encoding='utf8') as reader:
        curr_doc_key = ""
        # Know when to start and stop reading
        start_reading_text = False
        document = []

        for line in reader:
            # If detected an identifier for the documents
            if "<DOCNO>" in line:
                # Get the document identfier
                curr_doc_key = line.split('<DOCNO>')[1].split('</DOCNO>')[0]
            # If detected a beginning of a document
            if "<TEXT>" in line:
                # Toggle read mode
                start_reading_text = True
            # If detected end of a document
            if "</TEXT>" in line:
                start_reading_text = False
                documents[curr_doc_key] = " ".join([stemmer.stem(word) for word in document])
                document = []
            # If you are still reading the text
            if start_reading_text and "<TEXT>" not in line:  # Had to be included to avoid inserting "<TEXT>"
                # to the document
                document += [word for word in line.replace(',', '').replace('.', ''). replace('\n', '')
                             .replace('\t', '').split() if word != ""]
    return documents


def get_queries():
    """
    get_queries reads the queries file and return a queries data structure (dict)
    :return: dict of queries
    """
    queries = {}
    with open(constants.QUERIES_FILE) as reader:

        for line in reader:
            query_id = line.split(':')[0]
            query = line.split(':')[1].replace('\n', '')
            queries[query_id] = query

    return queries


def rel_kword_reader(file):

    """
    rel_kword_reader reads a relevance/keyword file and return a dict containing the scores
    :param file: file to be read
    :type file: str
    :return: dict of relevance/keyword scores
    """

    dictionary = {}

    with open(file) as reader:
        for line in reader:
            key = line.split()[2][6:]  # Remove EPOCH/ROUND
            score = line.split()[3][:1]  # Remove the '\n'
            dictionary[key] = score

    return dictionary


def get_relevance():

    """
    get_relevance reads the relevance file and return a relevance data structure (dict)
    :return: dict of relevance scores
    """

    return rel_kword_reader(constants.RELEVANCE_FILE)


def get_keywords():

    """
    get_keywords reads the relevance file and return a keywords data structure (dict)
    :return: dict of keyword scores
    """

    return rel_kword_reader(constants.KEYWORDS_FILE)

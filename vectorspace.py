# Andre Rodriguez
# andrerod

import sys
import preprocess
import operator
import pdb
from pathlib import Path
from collections import defaultdict

def formatRawData(raw):
    """Format raw data."""
    # load the stopwords:
    with open("stopwords", 'r') as input:
        stopwords = [line.replace('\n', '') for line in input]

    formatted_text = preprocess.removeSGML(raw)
    text_list = formatted_text.split('\n')
    while '' in text_list:
        text_list.remove('')
    formatted_list = [text.split() for text in text_list]
    formatted_list2 = list(map(str, preprocess.chain.from_iterable(formatted_list)))        
    extracted_tokens = preprocess.tokenizeText(formatted_list2)
    extracted_tokens = preprocess.removeStopWords(extracted_tokens, stopwords)
    return preprocess.stemWords(extracted_tokens)

def generateDocumentLengths(document_lengths, inverted_index):
    for w in inverted_index:
        if w == 'total-docs': continue
        # try:
        inverted_index[w]['idf'] = preprocess.math.log10(float(inverted_index['total-docs']) / float(inverted_index[w]['df']))
        # except KeyError:
            # inverted_index[w]['idf'] = preprocess.math.log10(inverted_index['d-count'] / inverted_index[w]['df'])
        for doc, tf in inverted_index[w]['dl']:
            idf_tf = inverted_index[w]['idf'] * tf
            try:
                document_lengths[doc] += preprocess.math.pow(idf_tf, 2)
            except KeyError:
                document_lengths[doc] = preprocess.math.pow(idf_tf, 2)
    return {doc: preprocess.math.sqrt(document_lengths[doc]) for doc in document_lengths}

def indexDocument(raw, weights_docs, inverted_index):
    """Add doc's data to the inverted index"""

    if weights_docs != 'tfc' and weights_docs != 'tf':
        print("This is not one of the weighting schemes allowed for this program.")
        print("Please choose tfx for doc scheme or tfidf for both query and doc schemes.")
        sys.exit(1)

    try:
        inverted_index['total-docs'] += 1
    except KeyError:
        inverted_index['total-docs'] = 1

    word_freq = defaultdict(preprocess.default_value)
    for token in formatRawData(raw):
        word_freq[token] += 1.0
    

    for w in word_freq:
        document_term_freq = [inverted_index['total-docs'], word_freq[w]]
        try:
            inverted_index[w]['dl'].append(document_term_freq)
            inverted_index[w]['df'] += 1.0
        except KeyError:
            inverted_index[w] = {'dl': [document_term_freq],'df': 1.0}
    
    return inverted_index

def retrieveDocuments(queries, inverted_index, weight_docs, weight_queries):
    """Fetches the documents."""
    query_freq = {}
    scores = {}
    q_length = 0.0
    a = 0.0
    b = 0.0
    max_tf = 0.0

    # Preprocesses the query
    for w in formatRawData(queries):
        try:
            query_freq[w] += 1.0
        except KeyError:
            query_freq[w] = 1.0
    
    for w in query_freq:
        if w in inverted_index:
            q_length += preprocess.math.pow(float(inverted_index[w]['idf']) * float(query_freq[w]), 2) if w in inverted_index else q_length
    q_length = preprocess.math.sqrt(q_length)

    if weight_docs == "tfc" and weight_queries == "tfx":
        a = 0.5
        b = 0.5
        max_tf = query_freq[max(query_freq, key= lambda x: query_freq[x])]
        
    elif weight_docs == "tf" and weight_queries == "idf":
        a = 1.0
        b = 2.0
        max_tf = 1.0

    for w in query_freq:
        try:
            inverted_index[w]['dl']
        except KeyError:
            # For terms that do not appear in the dictionary,
            # but in the query, ignore them
            continue
        for doc, tf in inverted_index[w]['dl']:
            score = float(query_freq[w]) * tf * preprocess.math.pow(float(inverted_index[w]['idf']), 2) * (
                a + (b * query_freq[w]) / max_tf)
            try:
                scores[doc] += score
            except KeyError:
                scores[doc] = score
    return scores
    

def generate_vectorspace():
    """Generates the vecetorspace."""
    weight_docs = sys.argv[1]
    weight_queries = sys.argv[2]
    input_path = Path(sys.argv[3])
    queries = sys.argv[4]
    score_list = []
    docs = [doc for doc in input_path.iterdir() if doc.is_file()]
    inverted_index = {}
    document_lengths = {}
    query_lookup = { 
    int(line.rstrip().split()[0]): 
    ' '.join(line.rstrip().split()[1:]) for line in open(queries)  
    }
    for doc in docs:
        raw = str()
        with open(doc, 'r', encoding='UTF-8') as read:
            for line in read: raw = raw + line
        if not raw: continue
        # add the formatted tokens to the inverted index:
        indexDocument(raw, weight_docs, inverted_index)
    document_lengths = generateDocumentLengths(document_lengths, inverted_index)
    for q_num, q_str in query_lookup.items():
        rd = retrieveDocuments(q_str, inverted_index, weight_docs, weight_queries)
        for doc, score in rd.items():
            score_list.append([q_num, doc, score])

    score_list.sort(key=operator.itemgetter(2), reverse=True)
    score_list.sort(key=operator.itemgetter(0))
    filename = "cranfield." + str(weight_docs) + "." + str(weight_queries) + ".output"
    with open(filename, "w", encoding='UTF-8') as w:
        for query_number, doc, score in score_list:
            w.write(str(query_number) + ' ' + str(doc) + ' ' + str(score) + '\n')

if __name__ == '__main__':
    """Main driver function for vectorspace.py."""
    generate_vectorspace()
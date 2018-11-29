""" to make the queries on the merged master file
"""
from argparse import ArgumentParser
from dictionary import BlockFile, BlockLine
from FileInformation import SetInfo, ArticleInfo

import os
SEARCH_FILES = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DISK'), 'Merged_withConstraints_v1.txt')
DATASET = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DISK'), 'dataset.txt')
INFO_FOR_QUERIES = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DISK'), 'infoForQueries.txt')
SENTIMENT = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DISK'), 'sentiment_for_each_url.txt')
import sys
import pprint
import operator
from math import log10
from afinn import Afinn

def setRanking(query_terms, arr_terms, url_list, set_data, article_data):
    ''' Analyse informations and process ranking with BM25

    Args: 
        query_terms -- list of query_terms from the query
        arr_terms -- res of all terms
        url_list: new_id of article with at least one keyword
        set_data: information from all the articles
        article_data: actual article information
    Return: ranked list
    '''
    K1 = float(0.5)
    B = float(0.5)
    
    sentiment_weight = float(0.5)
    bm25_weight = float(1.0) - sentiment_weight

    totalNumberOfArticles = set_data.article_count
    avgDL = set_data.avgDL

    doc_rankings = dict()

    # save query terms sentiment values
    afinn = Afinn()
    query_sentiments = {}
    for term in range(len(query_terms)):
        query_sentiments[str(query_terms[term])] = afinn.score(query_terms[term])

    for url_for_newID in url_list:
        result_article_info = article_data.getArticleInfo(url_for_newID)
        result_article_info = result_article_info.split(' ')
        article_length = result_article_info[1]

        doc_ranking_val = 0
        sentiment_ranking = 0
        for term in range(len(query_terms)):

            # get frequency
            doc_freq = arr_terms[term].get_document_frequency()
            termFrequency = arr_terms[term].get_term_frequency(url_for_newID)

            res_1 = float(totalNumberOfArticles) / doc_freq
            res_2 = (K1 + 1) * termFrequency

            # corner cases
            if termFrequency == 0:
                return 0

            # calculate the BM25
            res_3 = (K1 * ((1 - B) + B * (float(article_length) / avgDL)) + termFrequency)

            # adding log
            doc_ranking_val = log10(res_1 * res_2 / res_3)

            # calc sentiment ranking value
            if query_sentiments[str(query_terms[term])] < 0: # negative sentiment query term
                sentiment_ranking = float(-(result_article_info[2]))
            elif query_sentiments[str(query_terms[term])] > 0: # postive sentiment query term
                sentiment_ranking = float(result_article_info[2])
            else: # not negative or positive value would pass the sentiment weight to the bm25 ranking
                sentiment_ranking = doc_ranking_val
            
        doc_rankings[url_for_newID] = (bm25_weight * doc_ranking_val) + (sentiment_weight * sentiment_ranking)

    res = sorted(doc_rankings.items(), key=operator.itemgetter(1), reverse=True)
    return res

def queyOrInFiles(terms, block):
    ''' Search for elements in the files with the algorithm as describe in the book
    Args:
        terms: all terms that we are looking for
        block: path to block saved to disk
    '''
    query_terms_iter = iter(terms)
    current_term = query_terms_iter.__next__()   

    #get the file handle, default read of the files
    block.openMode()

    res = list()
    while current_term:
        # get the line
        line = block.readNextLineInBlockFile()
        if not line:
            #pprint.pprint("end")
            break
        if line.term < current_term:
            #print("line term:"+line.term+" -- current_term:"+current_term)
            continue
        elif line.term == current_term:
            #pprint.pprint("Recording a posting for: "+ current_term)
            #print("The line appened is:"+line)
            res.append(line)
        

        try:
            # try to find another one without exceptions
            current_term = query_terms_iter.__next__()
            #pprint.pprint("Looking for:"+current_term)
        except StopIteration:
            #print("end all")
            break

    res_postings = find_union([result.postings_list for result in res])
    setInfo = SetInfo()
    coll_info = setInfo.parse_info_file(DATASET)
    articleInfo = ArticleInfo()
    doc_info = articleInfo.parse_info_file(INFO_FOR_QUERIES)
    
    ranked_result = setRanking(terms, res, res_postings, coll_info, doc_info)

    # print result in a table
    from prettytable import PrettyTable
    RES = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DISK'), 'Result_01.txt')
    f= open(RES,"w+")
    my_table = PrettyTable()
    my_table.field_names = ["NEW_ID","RANK"]
    if ranked_result:
        for _id, result_tuple in enumerate(ranked_result):
            my_table.add_row([str(result_tuple[0]),str(result_tuple[1])])
        print(my_table)
        table_txt = my_table.get_string()
        f.write(table_txt)

    return ranked_result

def writeTableToFile(ranked_result):
    """ Helper method to save results to file
    """
    from prettytable import PrettyTable
    RES = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'DISK'), 'Result_01.txt')
    f= open(RES,"w+")
    my_table = PrettyTable()
    my_table.field_names = ["NEW_ID","RANK"]
    if ranked_result:
        for numb, result_tuple in enumerate(ranked_result):
            my_table.add_row([str(result_tuple[0]),str(result_tuple[1])])
        print(my_table)
        table_txt = my_table.get_string()
        f.write(table_txt)

def find_union(res):
    '''Find the union OR of a set
    '''
    if res:
        return sorted(set.union(*[set(l) for l in res]))
    else:
        return list()

def dispatchQuery(path, query_terms):
    ''' ALWAYS OR -- change from Assignment1 

    Args:
        path: path to the folder DISK
        terms: terms asked to search for by the user
        and_or_choice: between the terms is an AND or an OR
    '''
    query_terms = sorted(query_terms)
    dictionary_file = BlockFile(path) 
    res = None

    res = queyOrInFiles(query_terms, dictionary_file)
    
    return res

def run(args):
    ''' Running the commands on the files and printing the result

    Args:
        args: arguments passed in the command line by the user
    '''

    # compress the query
    from nltk.corpus import stopwords
    #from nltk.stem import PorterStemmer
    #ps = PorterStemmer()

    #path = args.searchFiles

    term_arr = args.terms
    #term_arr = term_arr.decode("utf-8")
    # should compress terms in array of terms
    #remove stopwords
    term_arr = [i for i in term_arr if i not in stopwords.words('english')]
    term_arr = [term.lower() for term in term_arr]

    res = dispatchQuery(SEARCH_FILES, term_arr)

    #print("NewID matching the search: ")
    #pprint.pprint(res)
    return res


def parseQuery(args):
    ''' Using argparse to parse the query of the user.

    Args: args is the input entered by the user in the command line.

    Return: an object that represent the arguments as a list/tuple
    '''
    parser = ArgumentParser(description="Hello! Please enter a query")
    parser.add_argument('terms', metavar='all the terms to look for ', nargs='+')
    parse_obj = parser.parse_args(args)
    return parse_obj

if __name__ == '__main__':
    ''' Main function that process everyting
    '''
    parsed_obj = parseQuery(sys.argv[1:])
    parsed_result = run(parsed_obj)

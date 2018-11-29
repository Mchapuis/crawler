import json
import pprint
from afinn import Afinn
import nltk 
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import io, os, sys
from FileInformation import SetInfo
from FileInformation import ArticleInfo
files_directory = os.path.dirname(os.path.realpath(__file__))
output_disk_directory = os.path.join(files_directory, 'DISK')
ARTICLE_INFO = os.path.join(output_disk_directory, "infoForQueries.txt")
DATASET = os.path.join(output_disk_directory, "dataset.txt")
SENTIMENT = os.path.join(output_disk_directory, "sentiment_for_each_url.txt")

class invertedIndex():

    def __init__(self):
        with open('items.json') as f:
            _data = f.read()
        self.data = json.loads(_data)
        #self.data = json.dumps(_data, ensure_ascii=True)
        #self.data = json.load(self.data)
        #pprint.pprint(self.data)

            
    
    def parser(self):
        afinn = Afinn()
        # total number of documents/pages
        doc_count = 0
        document_set = ArticleInfo()
        sentiment_set = ArticleInfo()
        # total tokens 
        arr_element = list()
        arr_sentiment = list()

        # loop throught all the json items
        for numb, page in enumerate(self.data):
            text = ""
            url = None
            for key in self.data[numb]:
                pairs = list()
                # find the sentiment for the article
                
                if key == 'text':
                    text = self.data[numb]['text']#.encode('utf8')
                if url is None and key == 'url':
                    url = self.data[numb]['url']#.encode('utf8')
                #if key == 'sentiment':
                #    sentiment = self.data[numb]['sentiment']

                # tokenize the text
                #arr_terms = word_tokenize(str(text))

                # removing punctuation also
                tokenizer = RegexpTokenizer(r'\w+')
                arr_terms = tokenizer.tokenize(str(text))

                # remove stopwords
                arr_terms = [i for i in arr_terms if i not in stopwords.words('english')]
                arr_terms = [i for i in arr_terms if i not in stopwords.words('french')]

                # remove charmap codec errors
                import re

                arr_terms = [re.sub(u"(\u2026|\u0153|\u2011|\u2018|\u2019|\u2014|\u201c|\u201d|\u2013|\xc0)", "'", i) for i in arr_terms]

                # remove numbers
                arr_terms = [t for t in arr_terms if not self.is_number(t)] 


                tokenizer = RegexpTokenizer(r'\w+')
                # number of tokens
                numb_token = len(arr_terms)

                # sentiment for all the terms
                #my_score = [afinn.score(i) for i in arr_terms]

                # term and the url
                token_pair = [(term, url) for term in arr_terms]

                # get the length of terms for this article
                document_set.addArticleInfo(str(url), numb_token, str(afinn.score(str(text))))
                # get the sentiment for the url
                # sentiment_set.addArticleInfo(str(url), afinn.score(str(text)))
                
                # add to list for later
                pairs.extend(token_pair)
                #sentiment_and_url.extend(my_sentiment)
            
                # find the fequency
                doc_count += 1

            arr_element.extend(pairs)
            
        avgdl = float(len(arr_element)) / doc_count

        # register information for later user
        collection = SetInfo(doc_count, len(pairs),avgdl)

        self.saveFileInformation(ARTICLE_INFO, document_set.myString())
        self.saveFileInformation(DATASET, collection.toString())
        # self.saveFileInformation(SENTIMENT, sentiment_set.myString())

        return arr_element
        

    def saveFileInformation(self, file_name, my_information):
        ''' helper method to save information about each document
        to be retreived later
        '''
        with open(file_name, 'w') as f:
            f.write(str(my_information))

    def is_number(self, term):
        try:
            int_value = int(term)
        except ValueError:
            return False
        else:
            return True

inv_index = invertedIndex()
index_arr = inv_index.parser()
#pprint.pprint(index_arr)

from spimi_inverter import Inverter
from spmi_merger import Merger
 # call the spmi inverter to apply the algorithm
inverter_obj = Inverter(index_arr, block_limit=10)
output_files = inverter_obj.spimi_inverter()

# call the spmi merger
merger_obj = Merger(output_files)
blocks_merged = merger_obj.merge()

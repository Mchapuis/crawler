from collections import OrderedDict

class ArticleInfo:

    def __init__(self):
        """Init function: create a set of documents
        """
        self.dic = dict()

    def addArticleInfo(self, newid, length):
        """ Add all informations 

        Args:
            newid: ID of article
            length: length of new article
        """
        element = Article(newid, length)
        self.dic[newid] = element.toString()

    def getArticleInfo(self, newid):
        """Get information from article if we give an id

        Args:
            newid: id of article
        Returns: information
        """
        newid = newid.rstrip()
        return self.dic[newid]

    def myString(self):
        """ Return a string: doc_id doc_length

        Return: a string representation of the document set.
        """
        ordered_docset = OrderedDict(sorted(self.dic.items()))
        my_str = ""
        for acticle_info in ordered_docset.values():
            my_str += str(acticle_info) 
            my_str += "\n"
        #my_str = [str(article_info) for article_info in ordered_docset.values()]
        print("my stirng is:"+ my_str)
        return my_str
    
    @classmethod
    def parse_info_file(cls, path):
        ''' 
        get info from path
        changing newid to url....?
        '''

        document = cls()

        with open(path) as f:
            rec_line = f.readlines()
        
        for line in rec_line:
            split = line.split(' ')
            url = split[0]
            lenght = int(split[1])
            document.addArticleInfo(url, lenght)
        return document


class Article:

    def __init__(self, newid, length):
        """ Info for one article

        Args:
            newid - ID of the article
            length - the length of the document.
        """
        self.newId = newid
        self.length = length

    def toString(self):
        """ return a string as newID length 
        """
        my_str = '{} {}'.format(str(self.newId), self.length)
        return my_str


class SetInfo:

    def __init__(self, article_count=0, token_count=0, avgDL=0):
        """ Information about articles collected

        Args:
            article_count: total nmbr of articles
            token_count: total numbr of tokens found
            avgDL: average length of all the documents
        """
        self.article_count = article_count
        self.token_count = token_count
        self.avgDL = avgDL

    def toString(self):
        """return string
        """
        str_repr = "Total_number_of_articles= {}\n".format(self.article_count)
        str_repr += "Total_number_of_Tokens= {}\n".format(self.token_count)
        str_repr += "Average_Token_number= {}\n".format(self.avgDL)
        return str_repr

    @classmethod
    def parse_info_file(cls, path):
        '''
        parse info from file to get the information saved earlier
        '''
        with open(path) as f:
            rec_lines = f.readlines()
        
        for line in rec_lines:
            _split = line.replace('\n', '')
            _split = _split.split('=')
            if _split[0] == "Total_number_of_articles":
                article_count = int(_split[1])
            elif _split[0] == "Total_number_of_Tokens":
                token_count = int(_split[1])
            elif _split[0] == "Average_Token_number":
                avgDL = float(_split[1])
        
        return cls(article_count, token_count, avgDL)


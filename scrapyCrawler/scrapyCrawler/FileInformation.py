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
        return self.dic[newid]

    def toString(self):
        """ Return a string: doc_id doc_length

        Return: a string representation of the document set.
        """
        ordered_docset = OrderedDict(sorted(self.dic.items()))
        my_str = [str(article_info) for article_info in ordered_docset.values()]
        return my_str

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
        str_repr = "Total number of articles ={}\n".format(self.article_count)
        str_repr += "Total number of Tokens={}\n".format(self.token_count)
        str_repr += "Average Token number={}\n".format(self.avgDL)
        return str_repr

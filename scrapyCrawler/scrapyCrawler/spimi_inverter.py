""" spmi inverter algorithm 
"""
import sys
import os

from dictionary import BlockFile, BlockLine

class Inverter:
    def __init__(self, index_arr, block_limit=500, directory="DISK"):
        """ implementation of the spimi inverter

        Args:
            index_arr: array of [term, newID] from the parser -- changed for project3
                -- now it is [term, url, sentiment score]
            block_limit: 500 articles is the default of the BLOCK sizes
            directory: name of the directory where the files are
            postings_list to record
        """
        self.index_iter = iter(index_arr)
        self.block_limit = block_limit
        self.block_prefix = 0
        self.directory = directory
        self.posting_lists = None

        if self.block_limit is None:
            self.block_limit = 500

    
    def spimi_inverter(self):
        """ spimi-invert algorithm
        """
        output_files = list()
        # simulating writing to disk
        memory_available = True

        while memory_available: 
            print("New loop, memory available")
            dictionary = dict()
            count = set()
            posting_lists = []
            try:
                while self.block_limit >= len(count):#len(dictionary) < self.block_limit:
                    # get the tuple [term, newID]

                    # NOTE: Here had many problems with intergers and many exceptions errors.
                    #       But in the end, the problem was form the parser itself. The array wasn't
                    #       a list of tuples and it created errors.
                    token = self.index_iter.__next__()
                    try:
                        if token[0] not in dictionary:
                            # return a new list with the token[0] as key
                            posting_lists = self.addToDictionary(dictionary, token[0])
                        # if the term exists, then get the empty dictionary list for that term
                        else:
                            posting_lists = self.getPostingsList(dictionary, token[0])
                    except:
                        print("error with: "+str(token[0]))
                    
                    # add a newID to the list
                    print("adding to posting list" + token[0])
                    try:
                        self.addToPostingsList(posting_lists, token[1])
                    except IndexError:
                        print("error with token")
                    
                    # add newID to list so we count number of articles
                    if token[1] not in count:
                        count.add(token[1])              

            except StopIteration:
                print("End of index_arr.next()")
                memory_available = False
            
            #print("postings list is now:{}".format(posting_lists))
            #print("dictionary is now:{}".format(dictionary))
            sorted_terms = self.sortTerms(dictionary)
            dict_file = self.writeBlockToDisk(sorted_terms, dictionary)
            self.block_prefix += 1
            output_files.append(dict_file)

            #test: reset posting list

        return output_files
    
    @staticmethod
    def addToDictionary(dictionary, term):
        """ Add the token to the dictionary
        
        Args:
            dic: the dictionnary to add the term to.
            token: token to be added.
        
        returns: a posting list that holds an empty list() so that ID's can be saved in
        """
        dictionary[term] = list()
        return dictionary[term]
    
    @staticmethod
    def getPostingsList(dictionary, token):
        """ Get the postings list of the specified term int he specified dictionary.
        
        Args:
            dic: the dictionnary to add the term to.
            token: token to be added.

        returns: the list() that the dictionary holds
        """
        return dictionary[token]
    
    @staticmethod
    def addToPostingsList(posting_lists, newID):
        """ Append the ID of the article to the particular term.

        Args: 
            postings_list: a list that holds all ID's of articles for a particular term
            newID: article ID
        """
        posting_lists.append(newID)
    
    @staticmethod
    def sortTerms(dictionary):
        """ Sort the terms in a specified dictionary
        
        Args: 
            dictionary the dictionary to sort.
        Return:
             A list containing all dictionary terms sorted lexicographically.
        """
        return [term for term in sorted(dictionary.keys())]

    def writeBlockToDisk(self, sorted_terms, dictionary):
        '''Write block(represented as a dictionary) to disk(represented as a file)
        in order
        
        Args:
            sorted_terms - the order in which to write the terms
            dictionary   - dictionary to write to disk
        
        Returns: the BlockFile to which the dictionary was written.
        '''
        # get the correct file name and path
        file_name = 'BLOCK{}.txt'.format(self.block_prefix)
        file_path = os.path.join(self.directory, file_name)
        
        # Create a block object
        block_file = BlockFile(file_path)
        block_file.openMode(mode='w')

        # 
        for term in sorted_terms:
            line = BlockLine(list(), term, dictionary[term])
            block_file.writeLine(line)

        block_file.close_handle()
        return block_file

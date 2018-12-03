"""To simulate a Read and Save to disk. Here we read and save files to a 
new directory called DISK. Each new files are called BLOCK1, BLOCK2, ... and 
the maximum size of these blocks are 500 reuters articles."""

class BlockFile():
    def __init__(self, file_path):
        """Create a directory called DISK if doesn't already exists. 
        Then create a simulation of write, read and save per blocks
        of 500 articles to disk. Each block is named BLOCK1, BLOCK2 etc.

        Args: 
            file_path : path to the block file
        """
        self.DIR = "DISK"
        self.FILE_NAME = "BLOCK"
        self.file_path = file_path
        self.file_handle = None
        self.count = 0
    
    def openMode(self, mode='r'):
        ''' opening the file asked

        Args: mode in which the user wants to use. 
            w: write, r: read, r+: read and write
        '''

        self.file_handle = open(self.file_path, mode)
        return self.file_handle
    
    def deleteFiles(self):
        '''to reset files in folder. Used to print the table'''

        import os
        count = 1
        line = self.file_handle.readline()
        while line != None:
            file_name = "BLOCK{}.txt".format(count)
            os.remove(file_name)
            count+=1

    
    def writeLine(self, block_line_obj):
        '''  write the line to file

        Args: block line object to write to block file
        '''
        if not isinstance(block_line_obj, str):
            self.file_handle.write(block_line_obj.getObjectAsAstring())
        else:
            self.file_handle.write(str(block_line_obj))
        # count the number of lines
        self.count += 1
    
    def readNextLineInBlockFile(self):
        ''' Read next line from file

        Returns: BlockLine object
        '''

        line = self.file_handle.readline()
        if line:
            return BlockLine.lineToString(-1, line)
        else:
            return None
    
    def close_handle(self):
        '''Close the file io
        '''
        self.file_handle.close()
    
class BlockLine:
    def __init__(self, block_index_list, term, postings_list):
        '''Init function for BlockLine object
        Args:
            block_index_list: index of the file 
            term: term for the line
            posting_listS: the postings list for the line
        '''

        self.block_index_list = block_index_list
        self.term = term
        self.postings_list = postings_list
    
    @classmethod
    def lineToString(cls, block_index_list, line):
        ''' split the line from a block file line
        Args:
            block_index_list: the document info where the line was
            line: line to be split
        
        return:
         an array containing [term, postings_list]
        '''
        split = line.split(' ')
        return cls(block_index_list,split[0],[doc_id for doc_id in split[1:]])
    
    def merge(self, new_file_line):
        ''' Merge this dic line with another

        Args: 
            new_file_line: another line from another file to merge

        Returns: 
            new BlockLine object with those elements
        '''
        new_block_file_index_list = sorted(self.block_index_list + new_file_line.block_index_list)
        new_postings_list = sorted(self.postings_list + new_file_line.postings_list)
        return BlockLine(new_block_file_index_list, self.term, new_postings_list)

    def getObjectAsAstring(self):
        """
        Represent the line object as a string.
        :return:
        """
        result = '{} {}\n'.format(self.term, ' '.join([str(url) for url in self.postings_list]))
        return result
    
    def get_document_frequency(self):
        """
        Get the number of documents in which the term appears from the collection.
        :return: the number of documents in which the term appears from the collection.
        """
        return len(self.postings_list)

    def get_term_frequency(self, url):
        """
        Get the frequency of the term in the document for the given document ID.
        Args:
            url: the document url
        Return: the number of occurrences of the term in the given document.
        """
        freq = 0
        for _url in self.postings_list:
            if _url == url:
                freq +=1
        #print("returning frequency "+ str(freq))
        return freq


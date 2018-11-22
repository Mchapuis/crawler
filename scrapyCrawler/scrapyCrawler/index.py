""" main file to run the parsing / invert and merge
"""
import os
import io
import sys
import argparse

from spimi_inverter import Inverter
from spmi_merger import Merger
from parser_reuters import ReutersParser
from prettytable import PrettyTable

reuters_files_directory = os.path.dirname(os.path.realpath(__file__))
output_disk_directory = os.path.join(reuters_files_directory, 'DISK')
reuters = os.path.join(reuters_files_directory, 'reuters21578')

if not os.path.exists(reuters):
    print("NO SUCH DIRECTORYYYY")
    exit

def run(args):
    '''Calling all elements to apply spimi algorithm
    '''
    #print("args.number looks like this:"+str(args))
    #parser_obj = ReutersParser(reuters, stemming=args.stemming, numbers=args.numbers, case_folding=args.case_folding, stopwords=args.remove_stopwords)
    parser_obj = ReutersParser(reuters, False, False, False, True)
    index_arr = parser_obj.parser()

    # call the spmi inverter to apply the algorithm
    inverter_obj = Inverter(index_arr, block_limit=args.block_limit)
    output_files = inverter_obj.spimi_inverter()

    # call the spmi merger
    merger_obj = Merger(output_files)
    blocks_merged = merger_obj.merge()
    
    # print result
    print("{} total terms".format(blocks_merged.count))


    return blocks_merged

def getQueriesArgs(args):
    ''' Get the queries that the user wants to apply to the reuters articles for compression
    Args: the arguments passed in the command line
    '''
    parser = argparse.ArgumentParser(description="Query the Reuters corpus.")
    parser.add_argument('-b', '--block_limit', type=int, help="The block size limit in number of articles")
    parser.add_argument('-s', '--stemming', action='store_true', help="Apply stemming")
    parser.add_argument('-r', '--remove_stopwords', action='store_true', help="Remove stopwords")
    parser.add_argument('-c', '--case_folding', action='store_true', help="Apply case folding")
    parser.add_argument('-n', '--numbers', action='store_true', help="Remove numbers")
    return parser.parse_args(args)

def deleteFiles():
    ''' Used to create the table. We need to delete the files before processing a new line
    '''
    for filename in os.listdir(output_disk_directory):
        #print(filename)
        if filename.startswith("BLOCK"): 
            if "BLOCK0.txt" == filename:
                #print("they")
            os.remove(os.path.join(output_disk_directory,filename))

if __name__ == '__main__':
    queries = getQueriesArgs(sys.argv[1:])
    run(queries)

    ### to draw table #### 
    """     
    from types import SimpleNamespace as Namespace
    import time
    import os

    #directory = os.path.join(output_disk_directory, "DISK")
    #file_path = os.path.join("DISK", file_name)

    my_table = PrettyTable()
    my_table.field_names = ["total count","block limit","compression type", "difference in % with row above","time in seconds"]

    # NEED TO CREATE NEW TABLE
    # TODO: also need to RANK terms -- the most important article NEWID should come first
    # --- it's just a matter of counting the newID's repetitions for each term and get the one with higher number

    # add a line in the table
    # record the count as #1

    start = time.time()
    block_1 = run(Namespace(block_limit=500, case_folding=False, numbers=False, remove_stopwords=False, stemming=False))
    end = time.time()
    my_table.add_row([block_1.count, 500, "removed nothing", (block_1.count / block_1.count),(end - start)])

    # delete the files in the folder
    deleteFiles()


    # add a second line in the table
    start = time.time()
    block_2 = run(Namespace(block_limit=500, case_folding=False, numbers=False, remove_stopwords=False, stemming=True))
    end = time.time()
    my_table.add_row([block_2.count, 500, "Stemming only", (block_2.count / block_1.count),(end - start)])
    # record the count as #2
    # calculate the difference between the two and add the difference in the table

    # delete the files in the folder
    deleteFiles()


    # add a third line in the table
    start = time.time()
    block_3 = run(Namespace(block_limit=500, case_folding=False, numbers=False, remove_stopwords=True, stemming=True))
    end = time.time()
    my_table.add_row([block_3.count, 500, "Stemming and stop_words", (block_3.count / block_2.count),(end - start)])
    # record the count as #3? -- or #1?
    # calculate the differnece

    # delete the files in the folder
    deleteFiles()

    # add a third line in the table
    start = time.time()
    block_4 = run(Namespace(block_limit=500, case_folding=False, numbers=True, remove_stopwords=True, stemming=True))
    end = time.time()
    my_table.add_row([block_4.count, 500, "Stemming, stop_words and numbers", (block_4.count / block_3.count),(end - start)])
    # record the count as #3? -- or #1?
    # calculate the differnece

    # delete the files in the folder
    deleteFiles()

    # add a third line in the table
    start = time.time()
    block_5 = run(Namespace(block_limit=500, case_folding=True, numbers=True, remove_stopwords=True, stemming=True))
    end = time.time()
    my_table.add_row([block_4.count, 500, "Stemming, stop_words and numbers", (block_5.count / block_4.count),(end - start)])
    # record the count as #3? -- or #1?
    # calculate the differnece

    # delete the files in the folder
    deleteFiles()
    print(my_table)

 
    start = time.time()
    block_1 = run(Namespace(block_limit=500, case_folding=False, numbers=False, remove_stopwords=False, stemming=False))
    end = time.time()
    my_table.add_row([block_1.count, 500, "removed nothing", (end - start)])
    print(my_table) 
    

    start = time.time()
    block_2 = run(Namespace(block_limit=250, case_folding=False, numbers=False, remove_stopwords=False, stemming=False))
    end = time.time()
    my_table.add_row([block_2.count, 250, "removed nothing", (end-start)])
    print(my_table) 

    start = time.time()
    block_3 = run(Namespace(block_limit=500, case_folding=False, numbers=False, remove_stopwords=False, stemming=True))
    end = time.time()
    my_table.add_row([block_3.count, 500, "stemming only", (end-start)])

    start = time.time()
    block_4 = run(Namespace(block_limit=100, case_folding=False, numbers=False, remove_stopwords=False, stemming=True))
    end = time.time()
    my_table.add_row([block_4.count, 100, "stemming only"], (end-start))

    start = time.time()
    block_5 = run(Namespace(block_limit=500, case_folding=False, numbers=False, remove_stopwords=True, stemming=True))
    end = time.time()
    my_table.add_row([block_5.count, 500, "stemming and stop-words", (end-start)])

    start = time.time()
    block_6 = run(Namespace(block_limit=100, case_folding=False, numbers=False, remove_stopwords=True, stemming=True))
    end = time.time()
    my_table.add_row([block_5.count, 100, "stemming and stop-words"], (end-start))
    
    start = time.time()
    block_7 = run(Namespace(block_limit=500, case_folding=True, numbers=True, remove_stopwords=True, stemming=True))
    end = time.time()
    my_table.add_row([block_7.count, 500, "case-folding, stemming, stop-words and numbers", (end-start)])
    """
    #print(my_table) 
    #print(my_table)
   


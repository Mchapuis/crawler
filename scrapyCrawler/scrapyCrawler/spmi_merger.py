""" merge all files into one by scanning each line of all files and comparing them
"""

import os
from dictionary import BlockFile, BlockLine
OUTPUT = "Merged_withConstraints_v1.txt"
class Merger:
    def __init__(self, block_files, directory='DISK'):
        """ This calss will merge all the files into one master merge file
        
        Args:
            block_files: the list of 'block' files to be merged.
            file_nmbr: the suffix number for the output files.
            directory: the output directory.
        """
        self.block_files = block_files
        self.directory = directory
        output_file_path = os.path.join(directory, OUTPUT)
        self.output_file = BlockFile(output_file_path)

    def merge(self):
        """ Takes each line of each files at a time. Then compare them and save the smallest.
        If they are the same, merge the NEWID's together. Then save to file

        Args: --
        Return: BlockFile representing the merged master file
        """

        """         
        all_files_handles = []
        for i in self.block_files:
            all_files_handles.append(i.openMode()) """

        # get all the file handles in an array
        BlockFile_handles = [f.openMode() for f in self.block_files]

        # set the file mode to write instead of read
        self.output_file.openMode(mode='w')

        # for each file handles, get the readline from the file
        next_lines = [f.readline() for f in BlockFile_handles]

        # while there are still any lines, loop
        while next_lines:

            # create a new object 
            next_line_to_write_to_file = BlockLine(list(), None, list())

            # using enumerate to get a counter with the list of lines
            for block_file_index, file_line in enumerate(next_lines):

                # get the line and save it as a string
                current_obj = BlockLine.lineToString([block_file_index], file_line)

                # if first line is empty then record it
                if next_line_to_write_to_file.term is None:
                    next_line_to_write_to_file = current_obj

                # if the term is equal to a line in the master, add the NEWID
                elif current_obj.term == next_line_to_write_to_file.term:
                    # recursive call 
                    next_line_to_write_to_file = current_obj.merge(next_line_to_write_to_file)

                # update the next_line_to_write_to_file to get the smallest possible
                elif current_obj.term < next_line_to_write_to_file.term:
                    next_line_to_write_to_file = current_obj

            # writing to file
            self.output_file.writeLine(next_line_to_write_to_file)

            #get the index
            next_line_index = next_line_to_write_to_file.block_index_list

            # get new lines for next loop
            new_next_lines = [BlockFile_handles[index].readline() for index in next_line_index]

            # loop throught the new lines with counter
            for index, next_new_line in enumerate(new_next_lines):
                # if empty, will throw an error
                try:
                    if not next_new_line:
                        # remove current file and next
                        del(next_lines[next_line_index[index]])
                        BlockFile_handles[next_line_index[index]].close()
                        del(BlockFile_handles[next_line_index[index]])
                    else:
                        next_lines[next_line_index[index]] = next_new_line
                except IndexError:
                    continue

        # close
        print("Merged file done")
        self.output_file.close_handle()
        return self.output_file

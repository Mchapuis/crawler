# cleaning up the merged file because there are too many new lines
import io

merged = open("new_merged_result.txt", "w")

LINE = None

with open(r"Merged_withConstraints_v1.txt", "r") as f:
    for line in f:
        line_split = line.split(" ")     
		
        # get last element
        # remove \n
        line_split[-1] = line_split[-1].replace('\n', '')

        # remove empty elements at the beginning of lines - if any
        line_split = list(filter(None, line_split))
		
        if not line_split:
            continue

        # if url - save it at the end of the line - exend the line with the new url
        if line_split[0][:4] == "http" and LINE is not None:
            LINE.extend(line_split)
			
        # if the element is not a url
        if "http" not in line_split[0] and LINE is not None:
            result = '{} {}\n'.format(str(LINE[0]),' '.join([str(url) for url in LINE[1:]]))
            merged.write(result)
            #reset
            LINE = None

        if LINE is None:
            LINE = line_split

merged.close()

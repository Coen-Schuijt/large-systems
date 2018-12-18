#!/usr/bin/env python3

import os
import sys

def get_args():
    try:
        path = sys.argv[1]
        return path
    except:
        print("Wrong arguments. Usage:\n./parse.py dir\ndir = Relative path to csv files")
        sys.exit(1)

def parser(path):
    
    ten_lines = []

    for entry in os.listdir(path):
        if entry.endswith('.csv'):
            if '_10_' in entry:
                
                with open(path + '/' + entry, 'r') as f:
                    lines = []
                    
                    for _ in range(6):
                        next(f)
                    for e, line in enumerate(f):
                        stripped_line = line.replace('\n','')
                        lines.append(stripped_line)
#                        print(e, line)

                    ten_lines.append(lines)
                    #print(lines)                        

            elif '_100_' in entry:
                pass
            elif '_200_' in entry:
                pass
            elif '_300_' in entry:
                pass

#    print(ten_lines)

#    for e,entries in enumerate(ten_lines):
        #print(e,entries)
#        for e,res in enumerate(entries):
#            print(e,res)



if __name__ == "__main__":
    path = get_args()

    parser(path)

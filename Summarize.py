import sys, getopt
import re
from tqdm import tqdm

queries = {}
totalQueries = 0
explicit = False

def addToQueries(query):
    query = re.sub("\s+\d+\s+Query\s+", "", query)

    if not explicit:
        query = re.sub("=\s'.*?'|=\s\d*", " = '*'", query)
        query = re.sub("LIKE\s'.*?'", "LIKE '*'", query)
        query = re.sub("IN\s\(.*?\)", "IN (*)", query)
        query = re.sub("IN\s\"(.*)\"", "IN \"*\"", query)
        query = re.sub("VALUES\n\s\(\'.*?\'\)", "VALUES (*)", query)
        query = re.sub("AND '.*' LIKE CONCAT", "AND '*' LIKE CONCAT", query)

    global totalQueries
    totalQueries = totalQueries + 1

    if query in queries:
        queries[query] = queries[query] + 1
    else:
        queries[query] = 1

def main(argv):

    input = argv.pop(0)
    global explicit

    while sys.argv:
        arg = sys.argv.pop(0)

        if re.search(r'^(-e|--explicit)$', arg):
            explicit = True

    with open(input) as f:

        queryOngoing = False

        query = ""

        for line in tqdm(f):

            if "Connect" in line:
                continue

            if "exit()" in line:
                continue

            if "Quit" in line:
                continue

            if "Query" in line:

                if queryOngoing:
                    addToQueries(query)
                    query = ""


                queryOngoing = True
                query = query + line
            elif queryOngoing:
                query = query + line
            else:
                query = ""
                queryOngoing = False
                addToQueries(query)
                query = ""
            
    print("Total queries: {}".format(totalQueries))
    print("\n")

    for i,x in sorted(queries.items(), key=lambda x: x[1], reverse=True):
        print("[{} - {:0.2f}%]: {}".format(x, (x/totalQueries)*100, i.replace("\n", "")))
    

if __name__ == "__main__":
    main(sys.argv[1:])

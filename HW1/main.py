import scrape

QUERY_FILE = '100QueriesSet2.txt'
JSON_FILE = 'result.json'

def main():
    queries = scrape.File.read_queries(QUERY_FILE)
    results = []
    for query in queries:
        result = scrape.SearchEngine.search(query)
        print(result)
        results.append(result)
    # Call the store_results function with the queries and the results
    scrape.File.store_results(queries, results, JSON_FILE)
    

if __name__ == '__main__':
    main()
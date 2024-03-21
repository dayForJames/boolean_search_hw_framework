#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import codecs
import sys
import json


class Index:
    def __init__(self, index_file):
        self._index_file: str = index_file
        self._inverted_index: dict = {}

    def MAP(self):
        with open(self._index_file, "r", encoding="utf-8") as doc:
            for line in doc:
                file_id, file_title, file = line.split("\t")

                file_id = file_id.strip(" \n")
                file_title = file_title.strip(" \n")
                file = file_title + " " + file.strip(" \n")

                # with open('./data/MAP_FILE.txt', 'w', encoding='utf-8') as map_file:
                #     for word in file.split(' '):
                #         is_valid = True

                #     #!  Maybe should rewrite
                #         for s in word:
                #             if not s.isascii():
                #                 is_valid = False
                #                 break

                #         if is_valid:
                #             map_file.write(word + ' ' + file_id + '\n')

                #     map_file.close()

                for word in file.split(" "):
                    is_valid = True

                    #!  Maybe should rewrite
                    for s in word:
                        if not s.isascii():
                            is_valid = False
                            break

                    if is_valid:
                        if word not in self._inverted_index.keys():
                            self._inverted_index[word] = set()

                        self._inverted_index[word].add(int(file_id[1:]))

            for key in self._inverted_index.keys():
                self._inverted_index[key] = list(self._inverted_index[key])

            with open("data/inverse_index.json", "w", encoding="utf-8") as f:
                json.dump(
                    self._inverted_index,
                )

    def SORT(self):
        pass


class QueryTree:
    def __init__(self, qid, query):
        # TODO: parse query and create query tree
        pass

    def search(self, index):
        # TODO: lookup query terms in the index and implement boolean search logic
        pass


class SearchResults:
    def add(self, found):
        # TODO: add next query's results
        pass

    def print_submission(self, objects_file, submission_file):
        # TODO: generate submission file
        pass


def main():
    # Command line arguments.
    parser = argparse.ArgumentParser(description="Homework: Boolean Search")
    parser.add_argument("--queries_file", required=True, help="queries.numerate.txt")
    parser.add_argument("--objects_file", required=True, help="objects.numerate.txt")
    parser.add_argument("--docs_file", required=True, help="docs.tsv")
    parser.add_argument(
        "--submission_file", required=True, help="output file with relevances"
    )
    args = parser.parse_args()

    # Build index.
    index = Index(args.docs_file)
    index.MAP()

    # Process queries.
    search_results = SearchResults()
    with codecs.open(args.queries_file, mode="r", encoding="utf-8") as queries_fh:
        for line in queries_fh:
            fields = line.rstrip("\n").split("\t")
            qid = int(fields[0])
            query = fields[1]

            # Parse query.
            query_tree = QueryTree(qid, query)

            # Search and save results.
            search_results.add(query_tree.search(index))

    # Generate submission file.
    search_results.print_submission(args.objects_file, args.submission_file)


if __name__ == "__main__":
    main()

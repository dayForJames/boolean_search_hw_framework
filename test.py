#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import codecs
import sys
import json
import numpy as np

from csv import writer


class Index:
    def __init__(self, index_file):
        self._index_file: str = index_file
        self._inverted_index: dict = {}
        self._line_count = 0
        self._map_file = "./data/MAP_FILE.txt"
        self._inv_index_file = "./data/inverse_index.json"

    def getFromFile(self):
        with open(self._inv_index_file, "r", encoding="utf-8") as f:
            self._inverted_index = json.load(f)

        for key in self._inverted_index.keys():
            self._inverted_index[key] = set(self._inverted_index[key])

    def __getitem__(self, token):
        return self._inverted_index[token]

    def get(self, key):
        if key in self._inverted_index.keys():
            return self._inverted_index[key]

        return set()

    def process(self):
        with open(self._index_file, "r", encoding="utf-8") as doc:
            for line in doc:
                file_id, file_title, file = line.split("\t")

                file_id = file_id.strip(" \n")
                file_title = file_title.strip(" \n")
                file = file_title + " " + file.strip(" \n")

                for word in file.split(" "):
                    if word not in self._inverted_index.keys():
                        self._inverted_index[word.lower()] = set()

                    self._inverted_index[word.lower()].add(int(file_id[1:]))

        for key in self._inverted_index.keys():
            self._inverted_index[key] = list(self._inverted_index[key])

        with open(self._inv_index_file, "w", encoding="utf-8") as f:
            json.dump(self._inverted_index, f, ensure_ascii=False)


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
    # index.process()
    index.getFromFile()

    # search_results = SearchResults()


if __name__ == '__main__':
    main()

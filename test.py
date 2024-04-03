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
        if token in self._inverted_index.keys():
            return self._inverted_index[token]

        return set()

    def get(self, key) -> set:
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


class Tokenizer:
    def __init__(self, request : str):
        self._infixExpr = request
        self._priority = {'(': 0, '|': 1, ' ': 3}

    def calc_poliz(self, tokens : list) -> str:
        stack = []
        result = []

        for i in range(len(tokens)):
            c = tokens[i]

            if '()| '.find(c) == -1:
                result.append(c)

            elif c == '(':
                stack.append(c)
            elif c == ')':
                while (len(stack) > 0 and stack[-1] != '('):
                    result.append(stack.pop())

                stack.pop()
            elif c in self._priority.keys():
                while len(stack) > 0 and (self._priority[stack[-1]] >= self._priority[c]):
                    result.append(stack.pop())

                stack.append(c)

        while len(stack) > 0:
            result.append(stack.pop())

        return result

    def tokenize(self) -> list[str]:
        """Take str request and return list of lexems and operands for next request processing"""

        operands = " |()"
        token_list = []
        i = 0

        while i < len(self._infixExpr):
            if self._infixExpr[i] not in operands:
                word = ""
                while i < len(self._infixExpr) and self._infixExpr[i] not in operands:
                    word += self._infixExpr[i]

                    i += 1

                token_list.append(word.lower())

            elif self._infixExpr[i] in operands:
                token_list.append(self._infixExpr[i])
                i += 1

        return token_list

    def and_split(self, tokens : list) -> list:
        splits = []

        first_pos = 0
        ind = 0

        brack_balance = 0

        while ind < len(tokens):
            if tokens[ind] == "(":

                brack_balance += 1
                ind += 1

            elif tokens[ind] == ")":
                brack_balance -= 1
                ind += 1

            elif tokens[ind] == " " and (brack_balance == 0):
                splits.append(tokens[first_pos:ind])
                first_pos = ind + 1
                ind += 1

            elif tokens[ind] == "|":
                ind += 1

            else:
                ind += 1
                pass  # we don't make splits insidde

        splits.append(tokens[first_pos:ind])

        return splits


class QueryTree:
    def __init__(self, qid, query):
        self._query = query
        self._qid = qid
        self._tokenizer = Tokenizer(query)

    def search(self, index):
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
    # index.process()
    index.getFromFile()

    search_results = SearchResults()

    # with codecs.open(args.queries_file, mode="r", encoding="utf-8") as queries_fh:
    #     for line in queries_fh:
    #         fields = line.rstrip("\n").split("\t")
    #         qid = int(fields[0])
    #         query = fields[1]

    #         # Parse query.
    #         query_tree = QueryTree(qid, query)

    #         # Search and save results.
    #         search_results.add(query_tree.search(index))
    #         break

    # # Generate submission file.
    # search_results.print_submission(args.objects_file, args.submission_file)

    t = Tokenizer('a|b (2|2|2 8)')
    i = {'a': [1, 2], 'b': [2, 4], '1': [5, 9]}
    index._inverted_index = i
    tokens = t.tokenize()
    split = t.and_split(tokens)

    print(split)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import codecs
import sys
import json
import numpy as np


class Index:
    def __init__(self, index_file):
        self._index_file: str = index_file
        self._inverted_index: dict = {}
        self._line_count = 0
        self._map_file = './data/MAP_FILE.txt'
        self._inv_index_file = "./data/inverse_index.json"

    def process(self):
        with open(self._index_file, "r", encoding="utf-8") as doc:
            for line in doc:

                file_id, file_title, file = line.split("\t")

                file_id = file_id.strip(" \n")
                file_title = file_title.strip(" \n")
                file = file_title + " " + file.strip(" \n")

                for word in file.split(" "):
                    # is_valid = True

                    #!  Russian word are missed
                    #!  Maybe should rewrite
                    # for s in word:
                    #     if not s.isascii():
                    #         is_valid = False
                    #         break

                    # if is_valid:
                    if word not in self._inverted_index.keys():
                        self._inverted_index[word] = set()

                        self._inverted_index[word].add(int(file_id[1:]))

            for key in self._inverted_index.keys():
                self._inverted_index[key] = list(self._inverted_index[key])

            with open(self._inv_index_file, "w", encoding="utf-8") as f:
                json.dump(
                    self._inverted_index,
                )

    def MAP(self):
        with open(self._index_file, "r", encoding="utf-8") as doc:
            with open(self._map_file, "w", encoding="utf-8") as map_file:
                for line in doc:
                    file_id, file_title, file = line.split("\t")

                    file_id = file_id.strip(" \n")
                    file_title = file_title.strip(" \n")
                    file = file_title + " " + file.strip(" \n")
                    
                    for word in file.split(' '):
                        # is_valid = True
                        #!  Russian word are missed
                        # #!  Maybe should rewrite
                        # for s in word:
                        #     if not s.isascii():
                        #         is_valid = False
                        #         break

                        # if is_valid:
                        map_file.write(word + ' ' + file_id + '\n')


    def _count_file_lines(self, file : str) -> int:
        count = 0

        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                count += 1

        return count


    def SORT(self):
        FILE_BUF_COUNT = 50

        self._line_count = self._count_file_lines(self._map_file)

        size = self._line_count // FILE_BUF_COUNT
        last_size = self._line_count - size * FILE_BUF_COUNT

        line_ind = 0

        size_arr = np.full_like(np.zeros(FILE_BUF_COUNT), size)
        if last_size != 0:
            size_arr[-1] = last_size

        print(size_arr)

        # for part_i in range()

def intersection(A : list[int], B : list[int]) -> list[int]:
    i = j = 0
    result = []

    A_ = sorted(A)
    B_ = sorted(B)

    while i < len(A_) and j < len(B_):
        if A_[i] < B_[j]:
            i += 1
        elif A_[i] > B_[j]:
            j += 1
        else:
            result.append(A_[i])
            i += 1
            j += 1

    addition = []

    if i < len(A_):
        addition = A_[i:]
    elif j < len(B_):
        addition = B_[j:]

    if len(addition) > 0:
        for el in addition:
            if el in A_ and el in B_ and el not in result:
                result.append(el)

    return result


def union(A : list[int], B : list[int]) -> list[int]:
    i = j = 0
    result = []

    A_ = A.copy()
    A_ = sorted(A_)

    B_ = B.copy()
    B_ = sorted(B_)

    while i < len(A_) and j < len(B_):
        if A_[i] < B_[j]:
            result.append(A_[i])
            i += 1
        elif A_[i] > B_[j]:
            result.append(B_[j])
            j += 1
        else:
            result.append(B_[j])
            i += 1
            j += 1

    addition = []

    if j < len(B_):
        addition = B_[j:]
    elif i < len(A_):
        addition = A_[i:]

    if len(addition) > 0:
        for el in addition:
            if el not in result:
                result.append(el)

    return result

OPERATORS = {
    "|": (1, lambda x, y: union(x, y)),
    " ": (2, lambda x, y: intersection(x, y)),
}

class QueryTree:
    def __init__(self, qid, query):
        self._query = query
        self._qid = qid
        self._token_list = self.tokenizer(self._query)
    

    def tokenizer(self, request : str) -> list[str]:
        '''Take str request and return list of lexems and operands for next request processing'''
    
        operands = " |()"
        token_list = []
        i = 0

        while i < len(request):
            if request[i] not in operands:
                word = ""
                while request[i] not in operands and i < len(request):
                    word += request[i]

                    i += 1

                token_list.append(word)

            elif request[i] in operands:
                token_list.append(request[i])
                i += 1

        return token_list
    
    def shunting_yard(parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while (
                    stack
                    and stack[-1] != "("
                    and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]
                ):
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()


    def calc(polish, index):
        stack = []
        for token in polish:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                answ = OPERATORS[token][1](index[x], index[y])
                index['ANSWER'] = answ
                stack.append("ANSWER")
            else:
                stack.append(token)
        return index[stack[0]]
    

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
    
    # index.MAP()
    # index.SORT()

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

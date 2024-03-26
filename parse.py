# ?  https://habr.com/ru/articles/273253/
# def eval_(formula):
#     def parse(formula_string):
#         number = ""
#         for s in formula_string:
#             if s in "1234567890.":
#                 number += s
#             elif number:
#                 yield float(number)
#                 number = ""
#             if s in OPERATORS or s in "()":
#                 yield s
#         if number:
#             yield float(number)

#     def shunting_yard(parsed_formula):
#         stack = []
#         for token in parsed_formula:
#             if token in OPERATORS:
#                 while (
#                     stack
#                     and stack[-1] != "("
#                     and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]
#                 ):
#                     yield stack.pop()
#                 stack.append(token)
#             elif token == ")":
#                 while stack:
#                     x = stack.pop()
#                     if x == "(":
#                         break
#                     yield x
#             elif token == "(":
#                 stack.append(token)
#             else:
#                 yield token
#         while stack:
#             yield stack.pop()

#     def calc(polish):
#         stack = []
#         for token in polish:
#             if token in OPERATORS:
#                 y, x = stack.pop(), stack.pop()
#                 stack.append(OPERATORS[token][1](x, y))
#             else:
#                 stack.append(token)
#         return stack[0]

#     return calc(shunting_yard(parse(formula)))

# print(eval_("12 0|3"))

def tokenize(request : str) -> list[str]:
    operands = " |()"

    token_list = []
    i = 0

    while i < len(request):
        if request[i] not in operands:
            word = ""
            while i < len(request) and request[i] not in operands:
                word += request[i]

                i += 1

            token_list.append(word)

        elif request[i] in operands:
            token_list.append(request[i])
            i += 1

    return token_list


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


request = "УНИВЕРСИТЕТ|(МГИМО МГУ)"
index = {'УНИВЕРСИТЕТ': [2, 10, 3], 'МГИМО': [10, 4, 1, 90], 'МГУ': [10, 90, 3], 'ANSWER': []}
token_list = tokenize(request)
index_request = token_list.copy()

inverse_polish_notation = shunting_yard(token_list)
print(calc(inverse_polish_notation, index))


# print(index_request)

OPERATORS = {
    "|": (1, lambda x, y: x or y),
    " ": (2, lambda x, y: x and y),
}

# ?  https://habr.com/ru/articles/273253/
def eval_(formula):
    def parse(formula_string):
        number = ""
        for s in formula_string:
            if s in "1234567890.":
                number += s
            elif number:
                yield float(number)
                number = ""
            if s in OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

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

    def calc(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                stack.append(OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0]

    return calc(shunting_yard(parse(formula)))

# print(eval_("12 0|3"))

def tokenize(request : str) -> list[str]:
    ru_en_symbols = (
        "abcdefghijklmnopqrstuvwxyz"
        + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        + ("abcdefghijklmnopqrstuvwxyz" + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя").upper()
    )
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

        if request[i] in operands:
            token_list.append(request[i])
            i += 1

    return token_list

request = 'Иван Андреевич|(Кот (Матроскин|Белый))'


print(tokenize(request))

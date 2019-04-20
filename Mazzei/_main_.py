from pathlib import Path
from nltk import CFG
import numpy
import Mazzei.Node as Node


def main():
    grammar_folder = Path.cwd() / "Grammar"
    grammar_file = grammar_folder / "YodaCFG.cfg"

    sentences = ["Tu avrai novecento anni di età",      #Novecento anni di età tu avrai
                 "Tu hai amici lì",                     #Amici hai tu lì
                 "Noi siamo illuminati",                #Illuminati noi siamo
                 "Tu hai molto da apprendere ancora",   #Molto da apprendere ancora tu hai
                 "Skywalker corre veloce",              #Veloce Skywalker corre
                 "Skywalker sarà tuo apprendista",      #Tuo apprendista Skywalker sarà
                 "Il lato oscuro è arduo da vedere",    #Arduo da vedere il lato oscuro è
                 "Frase volutamente non supportata dalla grammatica"]

    with open(grammar_file, encoding='utf-8') as file:
        grammar = CFG.fromstring(file.read())

    root = cky(sentences[6].split(), grammar)
    Node.Node.print_tree(root)


def cky(words: list, grammar: CFG):
    table_dimension = len(words) + 1
    table = numpy.ndarray(shape=(table_dimension, table_dimension), dtype=list)

    for j in range(1, table_dimension):
        table[j - 1, j] = list()
        table[j - 1, j].append(Node.Node(find_head_lr(words[j - 1], grammar), None, None))
        for i in reversed(range(0, j - 1)):
            table[i, j] = list()
            for k in range(i + 1, j):
                if table[i, k] is not None and table[k, j] is not None:
                    table[i, j].append(Node.Node(find_head_gr(list(table[i, k])[0], list(table[k, j])[0], grammar),
                                                 list(table[i, k])[0], list(table[k, j])[0]))

    cky_res = [x for x in list(table[0, table_dimension-1]) if str(x.data) == "S"]
    if cky_res:
        return cky_res[0]


def find_head_lr(word: str, grammar: CFG):
    lexical_rules = list((prod for prod in grammar.productions()
                         if len(prod.rhs()) == 1 and prod.rhs()[0] == word))
    if lexical_rules:
        return lexical_rules[0].lhs()


def find_head_gr(first: Node, second: Node, grammar: CFG):
    grammar_rules = list((prod for prod in grammar.productions()
                          if len(prod.rhs()) == 2 and first.data == prod.rhs()[0] and second.data == prod.rhs()[1]))

    if grammar_rules:
        return grammar_rules[0].lhs()


main()


import numpy as np
import pandas as pd
from termcolor import cprint
from os import path
from os import getcwd

PATH = path.abspath(path.join(getcwd(), "dict/GRE_8000_Words.txt"))


def read_gre():
    df = pd.read_csv(
        PATH,
        sep="\s+",
        encoding="utf-8",
        header=None,
        names=list('abcd'),
    )
    df = df.fillna("")
    df['c'] = df['c'].astype(str) + df['d'].astype(str)
    df = df.drop("d", axis=1)
    df.columns = ['word', 'pron', 'expl']
    return df


def get_word(word=""):
    global DF
    DF = read_gre()
    if word == "":
        sample = DF.sample(1)
    else:
        sample = DF[DF.word == word]
    return (sample.index.item(), sample.word.values[0],
            "[" + sample.pron.values[0] + "]", sample.expl.values[0])


def check_word(index: int, word: str):
    global DF
    DF = read_gre()
    if word == DF.iloc[index].word:
        cprint("Correct: " + str(index) + " " + word, "white", "on_green")
    else:
        cprint("Incorrect: " + str(index) + " " + word, "white", "on_red")


if __name__ == '__main__':
    index, word, pron, expl = get_word()
    cprint(pron + "\n" + expl, "grey", "on_white")
    check_word(index, word)
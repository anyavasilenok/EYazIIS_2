import spacy
from spacy import displacy
from pathlib import Path
from svglib.svglib import svg2rlg  # pip3 install svglib
from reportlab.graphics import renderPM

POS = {'ADJ': 'прилагательное',
       'ADP': 'адлог',
       'ADV': 'наречие',
       'AUX': 'вспомогательный глагол',
       'CONJ': 'союз',
       'CCONJ': 'сочиниельный союз',
       'INTJ': 'междометие',
       'NOUN': 'существительное',
       'NUM': 'числительное',
       'PART': 'частица',
       'PRON': 'местоимение',
       'PROPN': 'имя собственное',
       'PUNCT': 'знак препинания',
       'SCONJ': 'подчинительный союз',
       'SYM': 'символ',
       'VERB': 'глагол',
       'X': 'не определено',
       'SPACE': 'пробел',
       'DET': 'детерминатив'
       }


def create_pic(txt):
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(txt)
    svg = displacy.render(doc, style="dep")
    output_path = "dependecy\dependency_plot.svg"
    # output_path.open("w", encoding="utf-8").write(svg)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    drawing = svg2rlg(output_path)
    renderPM.drawToFile(drawing, r"dependecy\dependency_plot.png", fmt='PNG')


def get_dict_for_edit(txt):
    nlp = spacy.load("ru_core_news_sm")
    edit_dict = {}
    doc1 = nlp(txt)
    for token1 in doc1:
        edit_dict.update({f'{token1.text}': f'{token1.pos_}'})
    return edit_dict


def change_class_of_word(key, value, txt):
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(txt)
    for token in doc:
        if token.text == key:
            token.pos_ = value

    svg = displacy.render(doc, style="dep")
    output_path = r"dependecy\dependency_plot.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    drawing = svg2rlg(output_path)
    renderPM.drawToFile(drawing, r"dependecy\dependency_plot.png", fmt='PNG')


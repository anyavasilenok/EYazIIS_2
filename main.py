import spacy
from spacy import displacy
from pathlib import Path
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

if __name__ == "__main__":
    nlp = spacy.load("ru_core_news_sm")

    act = 0
    txt = "сколько книг в библиотеке?"
    doc = nlp(txt)
    redact_dict = {}
    while act != "9":
        for token in doc:
            print(token.text, token.pos_, token.dep_)
            redact_dict.update({f'{token.text}': f'{token.pos_}'})
        print(redact_dict)
        for word in redact_dict:
            print(word, redact_dict[word])
        print("Выберите действие: \n 1 - Поменять текст"
              "                   \n 2 - Редактировать надписи у стрелочек"
              "                   \n 3 - Редактировать надписи под словами"
              "                   \n 9 - выход")

        act = input()
        if act == "1":
            print("Введите новый текст: ")
            txt = input()
        if act == "2":
            print("Что вы хотите изменить: ")
            to_change = input()
            print("На что поменять: ")
            change_to = input()
            for token in doc:
                print(token.dep_)
                if token.dep_ == to_change:
                    token.dep_ = change_to
                print(token.dep_)
        if act == "3":
            print("Что вы хотите изменить: ")
            to_change = input()
            print("На что поменять: ")
            change_to = input()
            for token in doc:
                print(token.pos_)
                if token.pos_ == to_change:
                    token.pos_ = change_to
                print(token.pos_)

        svg = displacy.render(doc, style="dep")
        output_path = Path("./dependecy/dependency_plot.svg")
        output_path.open("w", encoding="utf-8").write(svg)

        drawing = svg2rlg(output_path)
        renderPM.drawToFile(drawing, './dependecy/dependency_plot.png', fmt='PNG')


from natural_language_editor import create_pic, get_dict_for_edit, change_class_of_word
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Label, ttk, Scrollbar, filedialog, Toplevel, LabelFrame, Frame
from PIL import ImageTk, Image
import PyPDF2
import pickle
from scrollableImage import ScrollableImage
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


ASSETS_PATH = "pics\\"
DEPENDECT_PATH = "dependecy\\"
PATH_FOR_SAVINGS = "saves\\"
DICTIONARY = []


def relative_to_assets(path: str):
    return ASSETS_PATH + path


def relative_to_dependecy(path: str):
    return DEPENDECT_PATH + path


# Функция для очистки treeview и textbox
def clear_everything():
    dependecy_image = PhotoImage(file=relative_to_dependecy("blank.png"))

    scrlb_img = ScrollableImage(window, image=dependecy_image, scrollbarwidth=15, width=570, height=360)

    scrlb_img.pack()

    scrlb_img.place(
        x=535,
        y=158,
        width=570.0,
        height=360.0)
    input_1.delete('1.0', 'end')


def ccreate_pic():
    text = input_1.get(1.0, 'end').replace('\n', '')
    create_pic(text)
    dependecy_image = PhotoImage(file=relative_to_dependecy("dependency_plot.png"))

    scrlb_img = ScrollableImage(window, image=dependecy_image, scrollbarwidth=10, width=570, height=360)

    scrlb_img.pack()

    scrlb_img.place(
        x=535,
        y=158,
        width=570.0,
        height=360.0)


# Загрузка текста из pdf файла в textbox
def load_pdf():
    filepath = filedialog.askopenfilename()
    if filepath != "":
        if filepath[-4::] != '.pdf':
            print('это не pdf')
        else:
            with open(filepath, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                text = ''
                for i in range(num_pages):
                    page = reader.pages[i]
                    text += page.extract_text()

                lines = text.splitlines()
                text = ' '.join(lines)
                input_1.insert('1.0', text)


# Созранение словаря в формате pickle
def save_dictionary():
    global save_entry
    file_name = save_entry.get(1.0, 'end').replace('\n', '')
    filepath = PATH_FOR_SAVINGS + '\\' + file_name + '.pickle'
    with open(filepath, 'wb') as file:
        pickle.dump(DICTIONARY, file)


def save_img():
    file_name = save_entry.get(1.0, 'end').replace('\n', '')
    filepath = PATH_FOR_SAVINGS + '\\' + file_name + '.png'
    output_path = r"dependecy\dependency_plot.svg"
    drawing = svg2rlg(output_path)
    renderPM.drawToFile(drawing, filepath, fmt='PNG')


# Окно добавления словоформы
def add_form_window():
    global is_pressed_first_form
    is_pressed_first_form = True
    global is_pressed_first_info
    is_pressed_first_info = True
    add_form_window = Toplevel(window)
    add_form_window.lift()
    add_form_window.geometry("610x310")
    add_form_window.configure(bg="#639EED")

    add_form_canvas = Canvas(
        add_form_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    add_form_canvas.place(x=0, y=0)
    add_form_canvas.create_rectangle(
        10.0,
        11.0,
        590.0,
        490.0,
        fill="#2969BE",
        outline="")

    add_form_canvas.create_text(
        172.0,
        51.0,
        anchor="nw",
        text="Редактировать",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    # Текстбокс для ввода словоформы
    global add_form_entry
    add_form_entry = Text(
        add_form_window,
        bd=0,
        wrap="word",
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )

    add_form_entry.insert('1.0', "Слово, Класс")
    add_form_entry.bind("<Button-1>", add_form_on_click)

    add_form_entry.place(
        x=72.0,
        y=99.0,
        width=296.0,
        height=35.0
    )

    # Текстбокс для ввода информации для словоформы
    add_form_canvas.create_text(
        72.0,
        152.0,
        anchor="nw",
        text="Напишите какое слово на какой класс\n хотите поменять в виде: 'Слово, Класс'",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    dict_tv = ttk.Treeview(add_form_window,
                           columns=("text", "pos_"),
                           selectmode="browse")

    dict_tv.place(
        x=450.0,
        y=11.0,
        width=150.0,
        height=290.0)

    dict_tv.heading('text', text="Слово", anchor='w')
    dict_tv.heading('pos_', text="Класс", anchor='w')

    dict_tv.column('#0', stretch=False, width=0)
    dict_tv.column('#1', stretch=False, width=100)
    dict_tv.column('#2', stretch=False, width=50)

    edit_dict = get_dict_to_edit_syntactic_analysis()
    for word in edit_dict:
        dict_tv.insert('', 'end', values=(f'{word}', f'{edit_dict[word]}'))

    button_image_13 = PhotoImage(
        file=relative_to_assets("button_13.png"))
    # sss
    button_13 = Button(
        add_form_window,
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=edit_syntactic_analysis,
        relief="flat"
    )
    button_13.place(
        x=72.0,
        y=216.0,
        width=296.0,
        height=39.0
    )
    add_form_window.resizable(False, False)
    add_form_window.mainloop()


def get_dict_to_edit_syntactic_analysis():
    txt = input_1.get(1.0, 'end').replace('\n', '')
    dict_edit = get_dict_for_edit(txt)
    return dict_edit


def edit_syntactic_analysis():
    txt = input_1.get(1.0, 'end').replace('\n', '')
    text_to_edit = add_form_entry.get('1.0', 'end').replace('\n', '')
    text_to_edit = text_to_edit.replace(" ", "")
    key = text_to_edit.partition(',')[0]
    value = text_to_edit.partition(',')[2]
    change_class_of_word(key, value, txt)
    dependecy_image = PhotoImage(file=relative_to_dependecy("dependency_plot.png"))

    scrlb_img = ScrollableImage(window, image=dependecy_image, scrollbarwidth=10, width=570, height=360)

    scrlb_img.pack()

    scrlb_img.place(
        x=535,
        y=158,
        width=570.0,
        height=360.0)


# Функция для удаления текста при нажатии на текстбокс (текстбокс для ввода словоформы)
def add_form_on_click(event):
    global add_form_entry
    global is_pressed_first_form
    if is_pressed_first_form is True:
        add_form_entry.delete("1.0", 'end')
        is_pressed_first_form = False
    else:
        pass


# Функция для удаления текста по нажатию на текстбокс (текстбокс для ввода информации для словоформы)
def add_info_on_click(event):
    global add_info_entry
    global is_pressed_first_info
    if is_pressed_first_info is True:
        add_info_entry.delete("1.0", "end")
        is_pressed_first_info = False
    else:
        pass


# Окно сохранения словаря
def save_dictionary_window():
    save_dictionary_window = Toplevel(window)
    save_dictionary_window.lift()
    save_dictionary_window.geometry("440x301")
    save_dictionary_window.configure(bg="#639EED")

    save_canvas = Canvas(
        save_dictionary_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    save_canvas.place(x=0, y=0)
    save_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    save_canvas.create_text(
        214.0,
        104.0,
        anchor="nw",
        text="\/",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    save_canvas.create_text(
        123.0,
        59.0,
        anchor="nw",
        text="Введите название файла",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    global save_entry
    save_entry = Text(
        save_dictionary_window,
        bd=0,
        wrap="word",
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    save_entry.place(
        x=72.0,
        y=143.0,
        width=296.0,
        height=33.0
    )

    save_canvas.create_text(
        217.0,
        98.0,
        anchor="nw",
        text="|",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    button_10 = Button(
        save_dictionary_window,
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=save_img,
        relief="flat"
    )
    button_10.place(
        x=72.0,
        y=204.0,
        width=296.0,
        height=39.0
    )
    save_dictionary_window.resizable(False, False)
    save_dictionary_window.mainloop()


# Окно редактирования treeview
def edit_dictionary_window(data):
    edit_dictionary_window = Toplevel(window)
    edit_dictionary_window.lift()
    edit_dictionary_window.geometry("440x301")
    edit_dictionary_window.configure(bg="#639EED")

    edit_canvas = Canvas(
        edit_dictionary_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    edit_canvas.place(x=0, y=0)
    edit_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    edit_canvas.create_text(
        214.0,
        104.0,
        anchor="nw",
        text="\/",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    edit_canvas.create_text(
        152.0,
        59.0,
        anchor="nw",
        text="Измените строку",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    global edit_entry
    edit_entry = Text(
        edit_dictionary_window,
        bd=0,
        wrap="word",
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    edit_entry.place(
        x=72.0,
        y=143.0,
        width=296.0,
        height=33.0
    )

    edit_entry.insert('1.0', data)

    edit_canvas.create_text(
        217.0,
        98.0,
        anchor="nw",
        text="|",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    button_image_11 = PhotoImage(
        file=relative_to_assets("button_11.png"))
    button_11 = Button(
        edit_dictionary_window,
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=save_editing,
        relief="flat"
    )
    button_11.place(
        x=72.0,
        y=204.0,
        width=296.0,
        height=39.0
    )
    edit_dictionary_window.resizable(False, False)
    edit_dictionary_window.mainloop()


# Окно загрузки (пдф текста/словаря)
def load_window():
    load_window = Toplevel(window)
    load_window.lift()
    load_window.geometry("440x301")
    load_window.configure(bg="#639EED")

    load_canvas = Canvas(
        load_window,
        bg="#639EED",
        height=301,
        width=440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    load_canvas.place(x=0, y=0)
    load_canvas.create_rectangle(
        10.0,
        11.0,
        430.0,
        289.0,
        fill="#2969BE",
        outline="")

    # # Загрузить словарь из файла
    # button_image_8 = PhotoImage(
    #     file=relative_to_assets("button_8.png"))
    # button_8 = Button(
    #     load_window,
    #     image=button_image_8,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=load_dict_from_file,
    #     relief="flat"
    # )
    # button_8.place(
    #     x=85.0,
    #     y=110.0,
    #     width=261.0,
    #     height=55.0
    # )

    load_canvas.create_text(
        159.0,
        59.0,
        anchor="nw",
        text="Окно загрузки",
        fill="#FFFFFF",
        font=("Inter", 16 * -1)
    )

    # Загрузить пдф
    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_9 = Button(
        load_window,
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=load_pdf,
        relief="flat"
    )
    button_9.place(
        x=85.0,
        y=145.0,
        width=261.0,
        height=56.0
    )
    load_window.resizable(False, False)
    load_window.mainloop()


# Функция редактирования treeview
def edit_item(event):
    # Получить выделенную строку в Treeview
    selected_item = vocabulary.focus()

    # # Получить значения ячеек выбранной строки
    values = vocabulary.item(selected_item)['values']
    values = [i.replace('\n', '') for i in values]
    data = f'{values[0]} {values[1]} {values[2]}'
    edit_dictionary_window(data)


# Функция сохранения изменений в treeview
def save_editing():
    selected_item = vocabulary.focus()
    global edit_entry
    data = edit_entry.get(1.0, 'end').split()
    print(data)
    third_column = ''
    for i in data[4::]:
        third_column = third_column + i + ' '
    vocabulary.set(selected_item, 0, data[0] + ' ' + data[1])
    vocabulary.set(selected_item, 1, data[2] + ' ' + data[3])
    vocabulary.set(selected_item, 2, third_column)


window = Tk()


window.geometry("1200x700")

img = Image.open(r"pics\фон.png")
width = 1200
height = 700
imag = img.resize((width, height), Image.LANCZOS)
image = ImageTk.PhotoImage(imag)
panel = Label(window, image=image)
panel.pack(side="top", fill="both")


canvas = Canvas(
    window,
    bg="#F2F2F2",
    height=700,
    width=1200,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

canvas.create_rectangle(
    57.0,
    0.0,
    1371.0,
    700.0,
    fill="#FFFFFF",
    outline="")

canvas.create_image(0, 0, anchor="nw", image=image)

canvas.create_rectangle(
    0.0,
    0.0,
    1200.0,
    53.0,
    fill="#2969BE",
    outline="")

# Кнопка сохранить
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=save_dictionary_window,
    relief="flat"
)

button_1.place(
    x=805.0,
    y=6.0,
    width=123.0,
    height=41.0
)

canvas.create_text(
    39.0,
    19.0,
    anchor="nw",
    text="Spacy",
    fill="#FFFFFF",
    font=("Inter", 14 * -1)
)

# Кнопка загрузить

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=load_window,
    relief="flat"
)
button_3.place(
    x=938.0,
    y=6.0,
    width=123.0,
    height=41.0
)

# Кнопка добавить
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))

button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=add_form_window,
    relief="flat"
)
button_4.place(
    x=539.0,
    y=7.0,
    width=123.0,
    height=41.0
)

# Кнопка очистить
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))

button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=clear_everything,
    relief="flat"
)
button_5.place(
    x=672.0,
    y=6.0,
    width=123.0,
    height=41.0
)

# Кнопка фильтрация
# button_image_6 = PhotoImage(
#     file=relative_to_assets("button_6.png"))
#
# button_6 = Button(
#     image=button_image_6,
#     borderwidth=0,
#     highlightthickness=0,
#     command=filter_dictionary_window,
#     relief="flat"
# )
# button_6.place(
#     x=1071.0,
#     y=6.0,
#     width=123.0,
#     height=41.0
# )

# Рамки текстбоксов
# Бэкграунд текста
canvas.create_rectangle(
    81.0,
    110.0,
    491.0,
    540.0,
    fill="#177BAF",
    outline="")


# Ввод текста
input_1 = Text(
    bd=0,
    wrap="word",
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
input_1.place(
    x=99.0,
    y=158.0,
    width=374.0,
    height=303.0
)

vocabulary = ttk.Treeview(
    columns=None,
    height=0,
    selectmode="browse"
)

# Картинка!
dependecy_image = PhotoImage(file=relative_to_dependecy("blank.png"))

scrlb_img = ScrollableImage(window, image=dependecy_image, scrollbarwidth=15, width=570, height=360)

scrlb_img.pack()

scrlb_img.place(
    x=535,
    y=158,
    width=570.0,
    height=360.0)

# Бэкграунд картинки
canvas.create_rectangle(
    515.0,
    110.0,
    1125.0,
    540.0,
    fill="#177BAF",
    outline="")


canvas.create_text(
    161.0,
    126.0,
    anchor="nw",
    text="Ввод текста на естественном языке",
    fill="#FFFFFF",
    font=("Inter", 14 * -1)
)

canvas.create_text(
    750.0,
    126.0,
    anchor="nw",
    text="Синтаксический анализ",
    fill="#FFFFFF",
    font=("Inter", 14 * -1)
)


# Составить словарь
button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))

button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=ccreate_pic,
    relief='flat'
)

button_7.place(
    x=99.0,
    y=479.0,
    width=369.0,
    height=41.0
)

window.resizable(False, False)
window.mainloop()

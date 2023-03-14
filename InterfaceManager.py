import json
from tkinter import *
from datetime import *


class note_obj:
    def __init__(self, title: str, text: str, times: int):
        self.title = title
        self.text = text
        self.time = times

def search_found(keywrd):
    found_screen = Tk()
    found_screen.configure(background="grey")
    found_screen.geometry("720x300")
    found_screen.resizable(False, False)

    mainframe = Frame(found_screen, background="grey")
    mainframe.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(mainframe, background="grey")
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = Scrollbar(mainframe, orient=VERTICAL, command=my_canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, background="grey")

    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    n = 0
    ns = 0
    with open("filtered_data_file.json") as complex_data:
        data = complex_data.read()
        numbers = json.loads(data)
    for i in range(len(numbers["notes"])):
        if numbers["notes"][i]["title"].__contains__(keywrd) or numbers["notes"][i]["text"].__contains__(keywrd):
            note_objct = note_obj(title=numbers["notes"][i]["title"], text=numbers["notes"][i]["text"], times=numbers[
                "notes"][i]["time"])
            if numbers["notes"][i]["title"] != "":
                answr = Button(second_frame, text=numbers["notes"][i]["title"], height=3, width=50,
                               background="#ffe6b3", command=lambda x=note_objct: note_interface(x))
            else:
                answr = Button(second_frame, text=numbers["notes"][i]["text"], height=3, width=50,
                               background="#ffe6b3", command=lambda x=note_objct: note_interface(x))
            if ns == 0:
                answr.grid(row=n, column=0)
                ns = ns + 1
            elif ns == 1:
                answr.grid(row=n, column=2)
                n = n + 1
                ns = ns - 1
        else:
            print(i)


def entr_keywrd(previous_window):
    search_screen = Tk()
    previous_window.destroy()
    search_screen.geometry("250x80")
    search_screen.configure(background="grey")

    entr = Entry(search_screen, width=41)
    btn = Button(search_screen, text="find", background="#61bdac", command=lambda: search_found(entr.get()))

    entr.grid(row=0, column=1)
    btn.grid(row=1, column=1)


def note_interface(obj: note_obj):
    def delit(objct: note_obj):
        if objct.title != "":
            with open("filtered_data_file.json") as complex_data:
                data = complex_data.read()
                numbers = json.loads(data)
                for i in range(len(numbers["notes"])-1):
                    print(type(numbers))
                    print(numbers["notes"][i]["text"])
                    if objct.title == numbers["notes"][i]["title"]:
                        del numbers["notes"][i]
            with open("filtered_data_file.json", "w") as f:
                json.dump(numbers, f, indent=2)

        else:
            if objct.text != "":
                with open("filtered_data_file.json") as complex_data:
                    data = complex_data.read()
                    numbers = json.loads(data)
                    for i in range(len(numbers["notes"])-1):
                        print("rex", objct.text, "sex", numbers["notes"][i]["text"])
                        if objct.text == numbers["notes"][i]["text"]:
                            del numbers["notes"][i]
                with open("filtered_data_file.json", "w") as f:
                    json.dump(numbers, f, indent=2)
            else:
                with open("filtered_data_file.json") as complex_data:
                    data = complex_data.read()
                    numbers = json.loads(data)
                    for i in range(len(numbers["notes"])-1):
                        if objct.title == numbers["notes"][i]["title"]:
                            del numbers["notes"][i]
                with open("filtered_data_file.json", "w") as f:
                    json.dump(numbers, f, indent=2)

    note_wndw = Tk()
    note_wndw.geometry("400x360")
    note_wndw.configure(background="#ffe6b3")
    mainmenu = Menu(note_wndw)
    note_wndw.config(menu=mainmenu)
    note_wndw.resizable(False, False)

    mainframe = Frame(note_wndw, background="grey")
    mainframe.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(mainframe, background="grey")
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = Scrollbar(mainframe, orient=VERTICAL, command=my_canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas, background="#ffe6b3")

    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    page_set = Menu(mainmenu, tearoff=0)
    page_set.add_command(label="Видалити нотатку(-)", command=lambda: delit(obj))

    title = Label(second_frame, text=obj.title, background="#ffe6b3", height=3, width=20)
    txt = Label(second_frame, text=obj.text, background="#ffe6b3", height=18, width=60, justify=LEFT)
    times = Label(second_frame, text=obj.time, background="#ffe6b3", height=3)

    title.grid(column=0, row=0)
    txt.grid(column=0, row=1)
    times.grid(column=0, row=7)

    mainmenu.add_cascade(label="Інструменти", menu=page_set)


rs = 1
rsk = 0
time_text = ""
new_text = ""
loop = 0
def add_to_json(title, txt, previous_window):
    global new_text
    now = datetime.now()
    previous_window.destroy()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    def rigt_txt(title, txt):
        global rs
        global new_text
        global time_text
        global loop
        global rsk
        if len(txt) > 50:
            if loop < len(txt)//50:
                if txt[loop * 50 - rs] == " ":
                    print(txt[(loop + 1) * 50 - rsk])
                    if txt[(loop + 1) * 50 - rsk] == " ":
                        time_text = txt[loop * 50:(loop + 1) * 50 - rsk]
                        new_text = new_text + "\n" + time_text
                        loop = loop + 1
                    else:
                        rsk = rsk + 1
                        rigt_txt(title, txt)
                else:
                    rs = rs + 1
                    rigt_txt(title, txt)
            if loop == len(txt)//50:
                time_text = txt[loop * 50 - 1:]
                new_text = new_text + "\n" + time_text
                loop = loop + 1
            if loop > len(txt)//50:
                pass
            else:
                rigt_txt(title, txt)


    rigt_txt(title, txt)
    wrtng_inf = {
        "title": title,
        "text": new_text,
        "time": dt_string
    }
    with open("filtered_data_file.json") as complex_data:
        data = complex_data.read()
        numbers = json.loads(data)
    x = numbers
    x["notes"].append(wrtng_inf)
    with open("filtered_data_file.json", "w") as f:
        json.dump(x, f, indent=2)
    my_starting_interface = AuthenticationInterface()


def add_notes(previous_window: Tk):
    add_screen = Tk()
    add_screen.geometry("400x300")
    add_screen.configure(background="grey")
    previous_window.destroy()

    title = Label(add_screen, text="Введіть заголовок:", background="grey")
    title_entry = Entry(add_screen, width=45)
    txt = Label(add_screen, text="Введіть текст замітки:", background="grey")
    txt_entry = Entry(add_screen, width=65)

    cnfrm_btn = Button(add_screen, text="Прийняти", command=lambda: add_to_json(title_entry.get(),
                                                                    txt_entry.get(), add_screen), background="#61bdac")

    title.grid(column=0, row=0)
    title_entry.grid(column=0, row=1)
    txt.grid(column=0, row=2)
    txt_entry.grid(column=0, row=3)
    cnfrm_btn.grid(column=0, row=4)


class AuthenticationInterface:

    def __init__(self):
        start_screen = Tk()
        start_screen.configure(bg="grey")
        start_screen.geometry("720x300")
        start_screen.resizable(False, False)
        mainmenu = Menu(start_screen)

        start_screen.config(menu=mainmenu)

        mainframe = Frame(start_screen)
        mainframe.pack(fill=BOTH, expand=1)

        my_canvas = Canvas(mainframe)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = Scrollbar(mainframe, orient=VERTICAL, command=my_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))

        second_frame = Frame(my_canvas, background="grey")

        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        page_set = Menu(mainmenu, tearoff=0)
        page_set.add_command(label="Додати нотатку(+)", command=lambda: add_notes(start_screen))
        page_set.add_command(label="Знати за словом", command=lambda: entr_keywrd(start_screen))

        mainmenu.add_cascade(label="Інструменти", menu=page_set)

        with open("filtered_data_file.json") as complex_data:
            data = complex_data.read()
            numbers = json.loads(data)
        n = 0
        ns = 0
        for i in range(len(numbers["notes"])):
            note_objct = note_obj(title=numbers["notes"][i]["title"], text=numbers["notes"][i]["text"], times=numbers[
                "notes"][i]["time"])
            if numbers["notes"][i]["title"] == "":
                text = numbers["notes"][i]["text"][0:50]
                note = Button(second_frame, text=text, height=6, width=50, command=lambda x=note_objct: note_interface(x))
                note.configure(bg="#ffe6b3")
            else:
                note = Button(second_frame, text=numbers["notes"][i]["title"], height=6, width=50, command=
                                                                                lambda x=note_objct: note_interface(x))
                note.configure(bg="#ffe6b3")
            if ns == 0:
                note.grid(row=n, column=0)
                ns = ns + 1
            elif ns == 1:
                note.grid(row=n, column=2)
                n = n + 1
                ns = ns - 1
        start_screen.mainloop()

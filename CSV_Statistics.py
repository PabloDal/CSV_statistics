from tkinter import *
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd


class Vista:

    dataframe = pd.DataFrame()

    def __init__(self, parent=None, **configs):
        #Main Frame
        self.myParent = parent
        self.myParent.geometry("500x500")
        #Frame
        self.Main_Frame = Frame(self.myParent, bg="#444")
        self.Main_Frame.pack(expand=YES, fill=BOTH)
        #Controles
        self.Control_Frame = Frame(self.Main_Frame, bg="Gray70",
        borderwidth=2, relief=RAISED)
        self.Control_Frame.pack(side=TOP, expand=NO, fill=BOTH, padx=7,
        pady=7)
        control_title = "Commands"
        Label(self.Control_Frame, text=control_title, bg="Gray10",
        fg="Gray70",
        justify=LEFT).pack(side=TOP, expand=NO, fill=X, anchor=W)
        self.controls = Frame(self.Control_Frame, bg="Gray10")
        self.controls.pack(side=TOP, expand=NO, fill=X)
        #Output
        self.output_window = Frame(self.Main_Frame, bg="Gray70",
        borderwidth=2, relief=RAISED)
        self.output_window.pack(side=BOTTOM, expand=YES, fill=BOTH,
        padx=7, pady=7)
        output_title = "Display"
        Label(self.output_window, text=output_title, bg="#222",
        fg="Gray70", justify=LEFT).pack(side=TOP, expand=NO, fill=X,
        anchor=W)
        self.output = Frame(self.output_window, bg="Gray70")
        self.output.pack(side=TOP, expand=YES, fill=BOTH)

    #Usa ReadCSVdata
    def CSV_Button(self, sep=','):
        browsebutton = Button(self.Control_Frame, text="Load CSV",
        command=(lambda: Vista.ReadCSVdata(self, sep)))
        browsebutton["width"] = 15
        browsebutton.pack(side=LEFT)

    #Usa ReadCSVdata
    def CSV_Button_semic(self, sep=';'):
        browsebutton = Button(self.Control_Frame, text="Load CSV semicolon",
        command=(lambda: Vista.ReadCSVdata(self, sep)))
        browsebutton["width"] = 15
        browsebutton.pack(side=LEFT)

    #Usa Stats_CSV
    def Stats_CSV_Button(self):
        browsebutton = Button(self.Control_Frame, text="Statistics",
        command=(lambda: Vista.Stats_CSV(self)))
        browsebutton["width"] = 15
        browsebutton.pack(side=RIGHT)

        #Usa Null_CSV
    def Null_CSV_Button(self):
        browsebutton = Button(self.Control_Frame, text="Incomplete values",
        command=(lambda: Vista.Null_CSV(self)))
        browsebutton["width"] = 15
        browsebutton.pack(side=RIGHT)

    def ReadCSVdata(self, sep):
        filename = askopenfilename()
        try:
            data = pd.read_csv(filename, sep=sep)
        except Exception:
            print('Wrong csv file path')
        else:
            Vista.dataframe = data
            Vista.View_csv(self, Vista.dataframe)
            print('Data loaded')

    def View_csv(self, data):
        pop = Tk()
        pop.configure(background="#ffffff")
        canvas = Canvas(pop, borderwidth=0, width=500, height=500,
        background="#ffffff")
        canvas_frame = Frame(canvas, background="#ffffff")
        vsb = Scrollbar(pop, orient="vertical", command=canvas.yview)
        hsb = Scrollbar(pop, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vsb.set)
        canvas.configure(xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=canvas_frame, anchor="nw")

        for i in range(0, len(data.index)):
            if i > 10:
                break
            c = 0
            for col in data.columns:
                b = Label(canvas_frame, text=data[col][i], background="#ffffff")
                b.grid(row=i, column=c, sticky='news', ipadx=1, ipady=1)
                c += 1

        def FrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas_frame.bind("<Configure>", lambda event,
        canvas=canvas: FrameConfigure(canvas))

    def Stats_CSV(self):
        for widget in self.output.winfo_children():
            widget.destroy()
        data = Vista.dataframe
        shape = data.shape
        cols = Label(self.output, text='Number of columns ' + str(shape[1]),
        justify=LEFT, bg="Gray70")
        cols.pack(side=TOP, anchor=W)
        rows = Label(self.output, text='Number of rows ' + str(shape[0]),
        bg="Gray70")
        rows.pack(side=TOP, anchor=W)
        for col in data.columns:
            t = data[col].dtype
            types = Label(self.output, bg="Gray70",
            text='Data type of ' + str(col) + ' is ' + str(t))
            types.pack(side=TOP, anchor=W)
            if (np.issubdtype(t, np.number)):
                means = Label(self.output, text=str(col) + ' mean: ' +
                str(data[col].mean()), bg="Gray70")
                means.pack(side=TOP, anchor=W)

    def Null_CSV(self):
        for widget in self.output.winfo_children():
            widget.destroy()
        data = Vista.dataframe
        nulls = Label(self.output, bg="Gray70", text=data.isnull().sum())
        nulls.pack(side=TOP, anchor=W)


if __name__ == "__main__":
    root = Tk()
    run = Vista(root)
    run.CSV_Button()
    run.CSV_Button_semic()
    run.Stats_CSV_Button()
    run.Null_CSV_Button()
    root.mainloop()
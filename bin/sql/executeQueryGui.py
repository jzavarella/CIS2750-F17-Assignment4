# /*
#  * CIS2750 F2017
#  * Assignment 4
#  * Jackson Zavarella 0929350
#  * This file creates the execute query GUI
#  * No code was used from previous classes/ sources
#  */

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox, filedialog, Radiobutton
import webbrowser


class QueryGui(tk.Tk):
    """docstring for QueryGui."""
    def __init__(self, sql, parent):
        tk.Tk.__init__(self)
        self.title("Execute Query") # Set the title of the application
        self.sqlDriver = sql
        self.parent = parent
        self.protocol('WM_DELETE_WINDOW', self.quitHandler)  # Ask the user if they really want to quit when they hit the x button
        self.MODES = [
        ("Display events ordered by start time", "SELECT * FROM EVENT ORDER BY start_time ASC"),
        ("Display events from organizer: ", "SELECT EVENT.start_time, EVENT.summary FROM EVENT INNER JOIN ORGANIZER ON EVENT.organizer=ORGANIZER.org_id WHERE ORGANIZER.name="),
        ("Something location", "RGB"),
        ("Enter organizer name to contact: ", "SELECT contact from ORGANIZER WHERE ORGANIZER.name="),
        ("Something alarms", "a"),
        ]
        self.geometry("900x1200") # Set the dimension of the window
        self.mainFrame = tk.Frame(self)
        self.organizerEntry = None
        self.organizerMailEntry = None
        self.initQueryView() # Make the file view
        self.initLogPanel() # Make the console
        self.mainFrame.pack(fill="both", expand=1)
        self.helpWidget = None

    def initQueryView(self):
        queryViewFrame = tk.Frame(self.mainFrame, bd=3, relief=SUNKEN)
        paddedFrame = tk.Frame(queryViewFrame) # Set a padding frame so we can pad the scroll bar and the treeview at the same time
        radioFrame = tk.Frame(paddedFrame)

        self.radioVar = tk.StringVar(master=self)
        self.radios = []
        self.radioFrames = []
        for text, mode in self.MODES:
            self.radioFrames.append(tk.Frame(radioFrame))
            self.radioFrames[-1].pack(anchor=W)
            if text == self.MODES[1][0]:
                self.organizerEntry = Entry(self.radioFrames[-1], bd=2, width=20)
                self.organizerEntry.pack(side=RIGHT)
                # radio = Radiobutton(self.radioFrames[-1], text=text, value=mode, command=self.updateQuery, variable=self.radioVar)
            elif text == self.MODES[3][0]:
                self.organizerMailEntry = Entry(self.radioFrames[-1], bd=2, width=20)
                self.organizerMailEntry.pack(side=RIGHT)
                # radio = Radiobutton(self.radioFrames[-1], text=text, value=mode, command=self.updateQuery, variable=self.radioVar)

            radio = Radiobutton(self.radioFrames[-1], text=text, value=mode, command=self.updateQuery, variable=self.radioVar)
            radio.pack(side=LEFT)
            self.radios.append(radio)
        self.radios[0].select() # select the first radio button
        radioFrame.pack(side=LEFT)

        rightFrame = tk.Frame(paddedFrame)

        queryFrame = tk.Frame(rightFrame)
        queryLabel = Label(queryFrame, text="Query: ")
        queryLabel.pack(side=LEFT)
        self.queryEntry = tk.Entry(queryFrame, bd=2, width=50)
        self.queryEntry.pack(side=RIGHT)
        self.queryEntry.bind("<Return>", lambda event: self.after(150, self.executeQuery))
        self.queryEntry.insert(0, self.radioVar.get()) # Set the default query
        buttonFrame = tk.Frame(rightFrame)
        submitButton = Button(buttonFrame, text="Execute Query", command=self.executeQuery)
        submitButton.pack(side=RIGHT)
        helpButton = Button(buttonFrame, text="Help", command=self.helpHandler)
        helpButton.pack(side=RIGHT)
        buttonFrame.pack(side=BOTTOM, anchor=E)
        queryFrame.pack(anchor=N)

        rightFrame.pack(side=RIGHT, anchor=N)
        paddedFrame.pack(fill="both", padx=10, pady=10)
        queryViewFrame.pack(fill="both")

    def helpHandler(self):
        if self.helpWidget != None:
            return

        def destroyHelpWidget(self):
            self.helpWidget.destroy()
            self.helpWidget = None

        self.helpWidget = Tk()
        self.helpWidget.protocol('WM_DELETE_WINDOW', lambda: destroyHelpWidget(self))
        self.helpWidget.title("Help")

        outputString = "DESCRIBE EVENT: \n"
        longest = 0
        lines = 1
        response = self.sqlDriver.execute("DESCRIBE EVENT")
        num_fields = len(self.sqlDriver.cursor.description)
        field_names = [i[0] for i in self.sqlDriver.cursor.description]

        outputString += str(field_names) + "\n"
        lines += 1
        for r in response:
            row = " | ".join(str(c) for c in r)
            if len(row) > longest:
                longest = len(row)
            outputString += row + "\n"
            lines += 1

        outputString += "\n\nDESCRIBE ORGANIZER: \n"
        lines += 4

        response = self.sqlDriver.execute("DESCRIBE ORGANIZER")
        num_fields = len(self.sqlDriver.cursor.description)
        field_names = [i[0] for i in self.sqlDriver.cursor.description]

        outputString += str(field_names) + "\n"
        lines += 1
        for r in response:
            row = " | ".join(str(c) for c in r)
            if len(row) > longest:
                longest = len(row)
            outputString += row + "\n"
            lines += 1

        text = Text(self.helpWidget, height=lines, width=longest)
        text.pack()
        text.insert(END, outputString)

        self.helpWidget.mainloop()

    def updateOrganizerQuery(self):
        self.queryEntry.delete(0, 'end')
        self.queryEntry.insert(0, self.radioVar.get() + '\'' + self.organizerEntry.get() + '\'')

    def updateQuery(self):
        self.queryEntry.delete(0, 'end')
        self.queryEntry.insert(0, self.radioVar.get())
        self.queryEntry.xview(END)

    def executeQuery(self):
        query = self.queryEntry.get()

        if self.radioVar.get() == self.MODES[1][1]:
            query = self.radioVar.get()
            if (self.organizerEntry.get() == "" or self.organizerEntry.get() == " ") and query[-1] == "=":
                self.log("Please enter the name of an organizer into the entry box")
                self.organizerEntry.focus_set()
                return

            query = query + '\'' + self.organizerEntry.get() + '\''
            self.queryEntry.delete(0, 'end')
            self.queryEntry.insert(0, query)
            self.queryEntry.xview(END)
        elif self.radioVar.get() == self.MODES[3][1]:
            query = self.radioVar.get()
            if (self.organizerMailEntry.get() == "" or self.organizerMailEntry.get() == " ") and query[-1] == "=":
                self.log("Please enter the name of an organizer into the entry box")
                self.organizerMailEntry.focus_set()
                return

            query = query + '\'' + self.organizerMailEntry.get() + '\''
            self.queryEntry.delete(0, 'end')
            self.queryEntry.insert(0, query)
            self.queryEntry.xview(END)
        try:
            response = self.sqlDriver.execute(query)

            self.log("Resposne from " + query + ": ")
            num_fields = len(self.sqlDriver.cursor.description)
            field_names = [i[0] for i in self.sqlDriver.cursor.description]
            self.log(str(field_names)) # Get the filed names of the query
            longest = 0
            for r in response:
                row = " | ".join(str(c) for c in r)
                if len(row) > longest:
                    longest = len(row)
                self.log(row)
                if self.radioVar.get() == self.MODES[3][1]:
                    self.log("Openening mail client to email " + row)
                    webbrowser.open("mailto:?to=" + row, new=1)
                    break
            self.log("=" * longest)
        except Exception as e:
            self.log(str(e))
            self.log("=" * len(str(e)))

    def initLogPanel(self):
        logFrame = tk.Frame(self.mainFrame) # Create a frame to house the console
        paddedFrame = tk.Frame(logFrame, bd=3, relief=SUNKEN) # Create a frame to put both the console and scrollbar in which allows padding
        buttonFrame = tk.Frame(logFrame)
        buttonFrame.pack(fill="x", padx=10)
        clearButton = Button(buttonFrame, text="Clear Log", command=lambda: self.clearLog())
        clearButton.pack(side=RIGHT)
        self.console = tk.Text(paddedFrame, wrap="word", state=DISABLED) # Disable editing of the text
        scrollbar = tk.Scrollbar(paddedFrame, command=self.console.yview) # Make a scrollbar and marry it to the frame
        scrollbar.pack(side="right", fill="y") # Pin the scrollbar to the right side and take up all room
        self.console.config(yscrollcommand=scrollbar.set) # Tell the text that it loves the scrollbar even though she is married ot the padding frame

        logFrame.pack(fill="both")
        paddedFrame.pack(fill="both", padx=10, pady=10)
        self.console.pack(side="left", fill="both", expand=True)
        self.console.bind("<1>", lambda event: self.console.focus_set()) # Allow the user to only copy text from the console

    def clearLog(self):
        self.console.config(state=NORMAL) # Allow editting
        self.console.delete(1.0, END)
        self.console.config(state=DISABLED) # Disable editting

    def quitHandler(self):
        self.parent.executeGUI = None
        self.destroy()

    def log(self, log):
        self.console.config(state=NORMAL) # Allow editting
        self.console.insert(END, log) # Push the log into the end of the console
        self.console.insert(END, "\n") # Push the log into the end of the console
        self.console.config(state=DISABLED) # Disable editting
        self.console.see(END) # Ensure the console is scrolled to the end
        print(log) # Log the log in the console as well

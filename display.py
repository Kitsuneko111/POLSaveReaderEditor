"""Display class and functions for a GUI"""
import datetime
import os
import tkinter as tk
import winfiletime
from tkinter import filedialog as fd
from typing import List, Union
import shutil

from reader import Reader
from util.save import Save
from writer import Writer


class Display:
    """
    Display class for handling GUI and associated methods
    """

    def __init__(self):
        self._window = tk.Tk()
        self._reader = Reader()
        self._writer = Writer()
        self._main = None
        self._mainsave = Save()
        self._compsave = Save()
        self.mode = "EDIT"
        self.mainvals = []
        self.compvals = []
        self._buttons = {
            "LEFT": [],
            "RIGHT": []
        }

    def run(self):
        """
        Run the GUI
        """
        self.__setupEditorGui()
        self._window.mainloop()

    def __setupMainGui(self):
        win = self._window
        if self._main:
            self._main.destroy()
            self._main = tk.Frame(win)
        frame = self._main = tk.Frame(win)
        frame.config(bd=1, relief=tk.GROOVE)
        frame.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(frame)
        left.config(bd=1, relief=tk.RIDGE, padx=2, pady=3)
        left.columnconfigure(0, weight=1)
        left.pack(fill=tk.BOTH, side=tk.LEFT)
        left_cont = tk.Frame(left)
        left_cont.pack(fill=tk.X, side=tk.TOP)

        self._editButton = tk.Button(left_cont, text="Edit", command=self.__setupEditorGui)
        self._editButton.pack(fill=tk.X, expand=True)
        self._compareButton = tk.Button(left_cont, text="Compare", command=self.__setupCompareGui)
        self._compareButton.pack(fill=tk.X, expand=True)

    def __setupToolbarGui(self, cont, save, side):
        but1 = tk.Button(cont, text="1", command=lambda: self.__buttonPress(lambda: self._reader.readFile(
            f'{os.getenv("APPDATA")}\\..\\LocalLow\\Wishfully\\Planet of Lana\\slot_0.sav', saveOverride=save),
                                                                            side, 0)
                         )
        but1.pack(fill=tk.X, expand=True, side=tk.LEFT)
        but2 = tk.Button(cont, text="2", command=lambda: self.__buttonPress(lambda: self._reader.readFile(
            f'{os.getenv("APPDATA")}\\..\\LocalLow\\Wishfully\\Planet of Lana\\slot_1.sav', saveOverride=save),
                                                                            side, 1)
                         )
        but2.pack(fill=tk.X, expand=True, side=tk.LEFT)
        but3 = tk.Button(cont, text="3", command=lambda: self.__buttonPress(lambda: self._reader.readFile(
            f'{os.getenv("APPDATA")}\\..\\LocalLow\\Wishfully\\Planet of Lana\\slot_2.sav', saveOverride=save),
                                                                            side, 2)
                         )
        but3.pack(fill=tk.X, expand=True, side=tk.LEFT)
        but4 = tk.Button(cont, text="Custom", command=lambda: self.__buttonPress(lambda: self.__openCustom(save),
                                                                                 side, 3))
        but4.pack(fill=tk.X, expand=True, side=tk.LEFT)
        self._buttons[side] = [but1, but2, but3, but4]

    def __buttonPress(self, action, side, button=4):
        action()
        if self.mode == "EDIT":
            self.__changeVals(self.mainvals, self._mainsave)
        if self.mode == "COMPARE":
            if side == "LEFT":
                self.__changeVals(self.mainvals, self._mainsave)
            else:
                self.__changeVals(self.compvals, self._compsave)
            if self._mainsave.version is not None and self._compsave.version is not None:
                self.__checkCompare()
        if button < len(self._buttons[side]):
            for but in self._buttons[side]:
                but["relief"] = tk.RAISED
            self._buttons[side][button]["relief"] = tk.SUNKEN

    def __checkCompare(self):
        for i in range(8):
            if type(self.mainvals[i]) != list:
                if self.mainvals[i]["text"] != self.compvals[i]["text"]:
                    self.mainvals[i]["fg"] = "red"
                    self.compvals[i]["fg"] = "red"
                else:
                    self.mainvals[i]["fg"] = "black"
                    self.compvals[i]["fg"] = "black"
            else:
                for j in range(3):
                    if self.mainvals[i][j]["text"] != self.compvals[i][j]["text"]:
                        self.mainvals[i][j]["fg"] = "red"
                        self.compvals[i][j]["fg"] = "red"
                    else:
                        self.mainvals[i][j]["fg"] = "black"
                        self.compvals[i][j]["fg"] = "black"

    def __changeVals(self, vals: List[Union[tk.Entry, tk.Label, List[tk.Entry]]], save):
        vals[0]["text"] = winfiletime.to_datetime(save.timestamp).strftime("%Y/%m/%d - %H:%M:%S")
        vals[1]["text"] = save.version
        vals[2]["text"] = datetime.datetime.utcfromtimestamp(save.elapsed).strftime("%Hh %Mm %Ss")
        vals[3]["text"] = str(save.deathcounter)
        if type(vals[4]) == tk.Entry:
            vals[4].delete(0, "end")
            vals[4].insert(0, str(save.slot + 1))
            vals[5].delete(0, "end")
            vals[5].insert(0, str(save.chapterId))
            vals[6].delete(0, "end")
            vals[6].insert(0, str(save.sceneId))
            vals[7][0].delete(0, "end")
            vals[7][0].insert(0, str(save.position[0]))
            vals[7][1].delete(0, "end")
            vals[7][1].insert(0, str(save.position[1]))
            vals[7][2].delete(0, "end")
            vals[7][2].insert(0, str(save.position[2]))
        else:
            vals[4]["text"] = str(save.slot + 1)
            vals[5]["text"] = str(save.chapterId)
            vals[6]["text"] = str(save.sceneId)
            vals[7][0]["text"] = str(save.position[0])
            vals[7][1]["text"] = str(save.position[1])
            vals[7][2]["text"] = str(save.position[2])

    def __openCustom(self, save):
        file = fd.askopenfilename(initialdir=f'{os.getenv("APPDATA")}\\..\\LocalLow\\Wishfully\\Planet of Lana\\',
                                  defaultextension="sav", filetypes=(("Save Files", "*.sav"), ("All Files", "*.*")))
        if file:
            self._reader.readFile(file, saveOverride=save)

    def __saveAs(self):
        file = fd.asksaveasfilename(initialdir=f'{os.getenv("APPDATA")}\\..\\LocalLow\\Wishfully\\Planet of Lana\\',
                                    defaultextension="sav", filetypes=(("Save Files", "*.sav"), ("All Files", "*.*")))
        if not file:
            return
        shutil.copy("./base.sav", file)
        self.__save(file)

    def __save(self, file):
        self._mainsave.chapterId = int(self.mainvals[5].get())
        self._mainsave.sceneId = int(self.mainvals[6].get())
        self._mainsave.position = [int(self.mainvals[7][0].get()),
                                   int(self.mainvals[7][1].get()),
                                   int(self.mainvals[7][2].get())]
        self._mainsave.slot = int(self.mainvals[4].get()) - 1
        self._writer.writeFile(file, saveOverride=self._mainsave)
        self.__buttonPress(lambda: self._reader.readFile(file, saveOverride=self._mainsave), "LEFT")

    def __setupEditorGui(self):
        self.mode = "EDIT"
        self.__setupMainGui()
        self._window.title("Planet of Lana Save Editor - Editing")
        self._editButton["relief"] = tk.SUNKEN
        right = tk.Frame(self._main)
        right.config(bd=1, relief=tk.SUNKEN)
        right.columnconfigure(1, weight=1)
        right.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        tools = tk.Frame(right)
        tools.config(bd=1, relief=tk.SUNKEN, padx=2, pady=3)
        tools.rowconfigure(0, weight=1)
        tools.pack(fill=tk.BOTH, side=tk.TOP)
        tools_cont = tk.Frame(tools)
        tools_cont.pack(fill=tk.X, side=tk.LEFT)

        self.__setupToolbarGui(tools, self._mainsave, "LEFT")
        tk.Button(tools, text="Save",
                  command=lambda: self.__save(self._reader.lastFile)) \
            .pack(fill=tk.X, expand=True, side=tk.LEFT)
        tk.Button(tools, text="Save As", command=self.__saveAs).pack(fill=tk.X, expand=True, side=tk.LEFT)
        tk.Button(tools, text="Backup", command=self.__backup).pack(fill=tk.X, expand=True, side=tk.LEFT)

        self.mainvals = self.__setupValsEntry(right)

    def __backup(self):
        if self._reader.lastFile:
            os.makedirs(os.path.dirname(self._reader.lastFile), exist_ok=True)
            shutil.copy(self._reader.lastFile,
                        f'{os.getenv("APPDATA")}\\..\\LocalLow\\Wishfully\\Planet of Lana\\backups\\'
                        f'{datetime.datetime.now().strftime("%Y%m%d - %H%M%S")}.sav')

    def __setupValsEntry(self, frame):
        column1 = tk.Frame(frame)
        column1.pack(fill=tk.BOTH, side=tk.LEFT)
        column2 = tk.Frame(frame)
        column2.pack(fill=tk.BOTH, side=tk.LEFT)
        row1 = tk.Frame(column1)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row1, text="Timestamp: ").pack(side=tk.LEFT)
        row1 = tk.Frame(column2)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        timestampEntry = tk.Label(row1, text=str(winfiletime.to_datetime(self._mainsave.timestamp)
                                                 .strftime("%Y/%m/%d - %H:%M:%S")
                                                 if self._mainsave.timestamp is not None else None))
        timestampEntry.pack(side=tk.LEFT)
        row2 = tk.Frame(column1)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row2, text="Deaths: ").pack(side=tk.LEFT)
        row2 = tk.Frame(column2)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        deathcounterEntry = tk.Label(row2, text=str(self._mainsave.deathcounter))
        deathcounterEntry.pack(side=tk.LEFT)
        row3 = tk.Frame(column1)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row3, text="Chapter: ").pack(side=tk.LEFT)
        row3 = tk.Frame(column2)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        chapterEntry = tk.Entry(row3)
        chapterEntry.insert(0, str(self._mainsave.chapterId))
        chapterEntry.pack(side=tk.LEFT)
        column3 = tk.Frame(frame)
        column3.pack(fill=tk.BOTH, side=tk.LEFT)
        tk.Label(column3, text="\t").pack(side=tk.LEFT)

        column1 = tk.Frame(frame)
        column1.pack(fill=tk.BOTH, side=tk.LEFT)
        column2 = tk.Frame(frame)
        column2.pack(fill=tk.BOTH, side=tk.LEFT)
        row1 = tk.Frame(column1)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row1, text="Version: ").pack(side=tk.LEFT)
        row1 = tk.Frame(column2)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        versionEntry = tk.Label(row1, text=self._mainsave.version)
        versionEntry.pack(side=tk.LEFT)
        row2 = tk.Frame(column1)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row2, text="Shrines: ").pack(side=tk.LEFT)
        row2 = tk.Frame(column2)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        shrineEntry = tk.Label(row2, text="WIP")
        shrineEntry.pack(side=tk.LEFT)
        row3 = tk.Frame(column1)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row3, text="Scene: ").pack(side=tk.LEFT)
        row3 = tk.Frame(column2)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        sceneEntry = tk.Entry(row3)
        sceneEntry.insert(0, str(self._mainsave.sceneId))
        sceneEntry.pack(side=tk.LEFT)
        column3 = tk.Frame(frame)
        column3.pack(fill=tk.BOTH, side=tk.LEFT)
        tk.Label(column3, text="\t").pack(side=tk.LEFT)

        column1 = tk.Frame(frame)
        column1.pack(fill=tk.BOTH, side=tk.LEFT)
        column2 = tk.Frame(frame)
        column2.pack(fill=tk.BOTH, side=tk.LEFT)
        row1 = tk.Frame(column1)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row1, text="Elapsed: ").pack(side=tk.LEFT)
        row1 = tk.Frame(column2)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        elapsedEntry = tk.Label(row1, text=str(datetime.datetime.utcfromtimestamp(self._mainsave.elapsed)
                                               .strftime("%Hh %Mm %Ss")
                                               if self._mainsave.elapsed is not None else None))
        elapsedEntry.pack(side=tk.LEFT)
        row2 = tk.Frame(column1)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row2, text="Slot: ").pack(side=tk.LEFT)
        row2 = tk.Frame(column2)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        slotEntry = tk.Entry(row2)
        slotEntry.insert(0, str(self._mainsave.slot + 1 if self._mainsave.slot is not None else None))
        slotEntry.pack(side=tk.LEFT)
        row3 = tk.Frame(column1)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row3, text="Position: ").pack(side=tk.LEFT)
        row3 = tk.Frame(column2)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        positionEntry = [tk.Entry(row3), tk.Entry(row3), tk.Entry(row3)]
        for i in range(3):
            positionEntry[i].insert(0, str(self._mainsave.position[i]))
            positionEntry[i].pack(side=tk.LEFT)

        return [
            timestampEntry, versionEntry, elapsedEntry, deathcounterEntry, slotEntry, chapterEntry, sceneEntry,
            positionEntry
        ]

    def __setupValsLabel(self, frame, save):
        column1 = tk.Frame(frame)
        column1.pack(fill=tk.BOTH, side=tk.LEFT)
        column2 = tk.Frame(frame)
        column2.pack(fill=tk.BOTH, side=tk.LEFT)
        row1 = tk.Frame(column1)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row1, text="Timestamp: ").pack(side=tk.LEFT)
        row1 = tk.Frame(column2)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        timestampEntry = tk.Label(row1, text=str(winfiletime.to_datetime(save.timestamp)
                                                 .strftime("%Y/%m/%d - %H:%M:%S")
                                                 if save.timestamp is not None else None))
        timestampEntry.pack(side=tk.LEFT)
        row2 = tk.Frame(column1)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row2, text="Deaths: ").pack(side=tk.LEFT)
        row2 = tk.Frame(column2)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        deathcounterEntry = tk.Label(row2, text=str(save.deathcounter))
        deathcounterEntry.pack(side=tk.LEFT)
        row3 = tk.Frame(column1)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row3, text="Chapter: ").pack(side=tk.LEFT)
        row3 = tk.Frame(column2)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        chapterEntry = tk.Label(row3, text=str(save.chapterId))
        chapterEntry.pack(side=tk.LEFT)
        column3 = tk.Frame(frame)
        column3.pack(fill=tk.BOTH, side=tk.LEFT)
        tk.Label(column3, text="\t").pack(side=tk.LEFT)

        column1 = tk.Frame(frame)
        column1.pack(fill=tk.BOTH, side=tk.LEFT)
        column2 = tk.Frame(frame)
        column2.pack(fill=tk.BOTH, side=tk.LEFT)
        row1 = tk.Frame(column1)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row1, text="Version: ").pack(side=tk.LEFT)
        row1 = tk.Frame(column2)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        versionEntry = tk.Label(row1, text=save.version)
        versionEntry.pack(side=tk.LEFT)
        row2 = tk.Frame(column1)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row2, text="Shrines: ").pack(side=tk.LEFT)
        row2 = tk.Frame(column2)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        shrineEntry = tk.Label(row2, text="WIP")
        shrineEntry.pack(side=tk.LEFT)
        row3 = tk.Frame(column1)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row3, text="Scene: ").pack(side=tk.LEFT)
        row3 = tk.Frame(column2)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        sceneEntry = tk.Label(row3, text=str(save.sceneId))
        sceneEntry.pack(side=tk.LEFT)
        column3 = tk.Frame(frame)
        column3.pack(fill=tk.BOTH, side=tk.LEFT)
        tk.Label(column3, text="\t").pack(side=tk.LEFT)

        column1 = tk.Frame(frame)
        column1.pack(fill=tk.BOTH, side=tk.LEFT)
        column2 = tk.Frame(frame)
        column2.pack(fill=tk.BOTH, side=tk.LEFT)
        row1 = tk.Frame(column1)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row1, text="Elapsed: ").pack(side=tk.LEFT)
        row1 = tk.Frame(column2)
        row1.pack(fill=tk.BOTH, side=tk.TOP)
        elapsedEntry = tk.Label(row1, text=str(datetime.datetime.utcfromtimestamp(save.elapsed)
                                               .strftime("%Hh %Mm %Ss")
                                               if save.elapsed is not None else None))
        elapsedEntry.pack(side=tk.LEFT)
        row2 = tk.Frame(column1)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row2, text="Slot: ").pack(side=tk.LEFT)
        row2 = tk.Frame(column2)
        row2.pack(fill=tk.BOTH, side=tk.TOP)
        slotEntry = tk.Label(row2, text=str(save.slot + 1 if save.slot is not None else None))
        slotEntry.pack(side=tk.LEFT)
        row3 = tk.Frame(column1)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        tk.Label(row3, text="Position: ").pack(side=tk.LEFT)
        row3 = tk.Frame(column2)
        row3.pack(fill=tk.BOTH, side=tk.TOP)
        positionEntry = [tk.Label(row3, text=str(save.position[i])) for i in range(3)]
        for i in range(3):
            positionEntry[i].pack(side=tk.LEFT)

        return [
            timestampEntry, versionEntry, elapsedEntry, deathcounterEntry, slotEntry, chapterEntry, sceneEntry,
            positionEntry
        ]

    def __setupCompareGui(self):
        self.mode = "COMPARE"
        self.__setupMainGui()
        self._window.title("Planet of Lana Save Editor - Comparing")
        self._compareButton["relief"] = tk.SUNKEN
        main = tk.Frame(self._main)
        main.config(bd=1, relief=tk.SUNKEN)
        main.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        left = tk.Frame(main)
        left.config(bd=1, relief=tk.FLAT)
        left.columnconfigure(1, weight=1)
        left.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        mid = tk.Frame(main)
        mid.config(bd=1, relief=tk.FLAT)
        mid.pack(fill=tk.BOTH, side=tk.LEFT)
        tk.Label(mid, text="\t").pack()

        right = tk.Frame(main)
        right.config(bd=1, relief=tk.FLAT)
        right.columnconfigure(1, weight=1)
        right.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        lefttools = tk.Frame(left)
        lefttools.config(bd=1, relief=tk.SUNKEN, padx=2, pady=3)
        lefttools.rowconfigure(0, weight=1)
        lefttools.pack(fill=tk.BOTH, side=tk.TOP)
        lefttools_cont = tk.Frame(lefttools)
        lefttools_cont.pack(fill=tk.X, side=tk.LEFT)

        righttools = tk.Frame(right)
        righttools.config(bd=1, relief=tk.SUNKEN, padx=2, pady=3)
        righttools.rowconfigure(0, weight=1)
        righttools.pack(fill=tk.BOTH, side=tk.TOP)
        righttools_cont = tk.Frame(righttools)
        righttools_cont.pack(fill=tk.X, side=tk.RIGHT)

        self.__setupToolbarGui(lefttools, self._mainsave, "LEFT")

        self.__setupToolbarGui(righttools, self._compsave, "RIGHT")

        self.mainvals = self.__setupValsLabel(left, self._mainsave)
        self.compvals = self.__setupValsLabel(right, self._compsave)

        self.__checkCompare()


if __name__ == '__main__':
    display = Display()
    display.run()

# TODO - convert reader.py constant script to GUI base
# TODO - add types and comments and like useful stuff
# TODO - backup button

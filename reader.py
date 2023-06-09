"""Reader class and functions for reading values from a save file"""
import os
import time
from typing import Optional, List, Union, Dict, Tuple, Any, NoReturn

from util.locations import locations
from util.save import Save
from util.hexextendor import hexExtendor


class Reader:
    """
    Reader class to handle data reading
    """
    def __init__(self, save: Optional[Save] = None):
        self.save = save if save else Save()
        self.__locations = locations

    def readFile(self, file, saveOverride: Optional[Save] = None) -> Save:
        """
        Read the given file and save the data
        :param file: File to open and store data from
        :param saveOverride: Override for where data is stored from
        :return: Save file
        """
        if saveOverride:
            saveObject = saveOverride
        else:
            saveObject = self.save

        savefile = open(file, "r")
        for location in self.__locations:
            savefile.seek(location[0])
            data = savefile.read(location[1])
            hexdata = ""
            for datum in data:
                hexdata += hexExtendor(ord(datum), 2)
            saveObject.set(location[0], hexdata)
        savefile.close()
        return saveObject

    def _compare(self, new: Save, old: Optional[Save] = None) -> List[str]:
        """
        Compare two save objects for a change in value
        :param new: New save  file to compare to
        :param old: Old save file to compare to. Ignore to use stored save.
        :return: Changed attributes
        """
        changed = []
        if not old:
            old = self.save
        if old.timestamp != new.timestamp:
            changed.append("timestamp")
        if old.version != new.version:
            changed.append("version")
        if old.elapsed != new.elapsed:
            changed.append("elapsed")
        if old.deathcounter != new.deathcounter:
            changed.append("deathcounter")
        if old.slot != new.slot:
            changed.append("slot")
        if old.chapterId != new.chapterId:
            changed.append("chapterId")
        if old.sceneId != new.sceneId:
            changed.append("sceneId")
        if old.position != new.position:
            changed.append("position")
        return changed

    def compare(self, new: Union[str, Save], old: Optional[Union[str, Save]] = None) \
            -> Dict[str, Tuple[Any, Any]]:
        """
        Compare two files or saves for changes and return their values if so.
        :param new: File or save object
        :param old: File or save object. Ignore to use stored save.
        :return: Dict of changes {change: (old, new)}
        """
        if not old:
            oldSave = self.save
        elif type(old) == str:
            oldSave = Save()
            oldSave = self.readFile(old, oldSave)
        else:
            oldSave = old
        if type(new) == str:
            newSave = Save()
            newSave = self.readFile(new, newSave)
        else:
            newSave = new

        diffs = self._compare(newSave, oldSave)
        changes = {}
        for diff in diffs:
            changes[diff] = (oldSave.__getattribute__(diff), newSave.__getattribute__(diff))
        return changes

    def run(self) -> NoReturn:
        """
        Run the reader in a continuous mode as a console script.
        """
        self._constantCompare()

    def _constantCompare(self) -> NoReturn:
        """
        Constantly compare the current file with the last every 10 seconds.
        """
        ignoreTime = input("Would you like to ignore the time values?\n(Timestamp, Elapsed)\n(y/n) >>> ")
        while ignoreTime != "y" and ignoreTime != "n":
            ignoreTime = input("Would you like to ignore the time values?\n(Timestamp, Elapsed)\n(y/n) >>> ")
        slot = input("Which slot would you like to monitor?\n(1/2/3) >>> ")
        while not slot.isdigit() and (1 > int(slot) or int(slot) > 3):
            slot = int(input("Which slot would you like to monitor?\n(1/2/3) >>> "))
        slot = str(int(slot)-1)
        saveLocation = f'{os.getenv("APPDATA")}\\..\\LocalLow\\Wishfully\\Planet of Lana\\slot_{slot}.sav'
        save = self.readFile(saveLocation)
        slot = int(slot)
        if save.slot != slot:
            print("Chosen slot does not align with save's stored slot. This may cause artefacts such as no updates.")
        while True:
            try:
                newSave = Save()
                save = self.readFile(saveLocation, newSave)
                changes = self.compare(save)
                if ignoreTime == "y":
                    if "elapsed" in changes:
                        changes.pop("elapsed")
                    if "timestamp" in changes:
                        changes.pop("timestamp")
                if len(changes):
                    for change in changes:
                        print(f'{change.capitalize()}: {changes[change][0]} -> {changes[change][1]}')
                else:
                    print("No changes")
                self.save = newSave
                time.sleep(10)
            except KeyboardInterrupt:
                print("Exited")
                quit(0)


if __name__ == "__main__":
    if os.path.exists("test.sav"):
        reader = Reader()
        testSave = reader.readFile("test.sav")
        assert testSave.deathcounter == 1, \
            "read file death fail. Got "+str(testSave.deathcounter)+" instead"
        del reader

    reader = Reader()
    reader.run()

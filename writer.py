"""
Writer class and functions for saving data back into a save file
"""
import random
from typing import Optional

from util.locations import locations
from util.save import Save


class Writer:
    """
    Writer class to handle data saving
    """
    def __init__(self, save: Optional[Save] = None):
        self.save = save if save else Save()
        self.__locations = locations

    def writeFile(self, file, key: Optional[str] = None, saveOverride: Optional[Save] = None) -> Save:
        """
        Write the data to the given file and save the data
        :param file: File to open and store data into
        :param key: Optional specific value to save
        :param saveOverride: Override for where to source the data
        :return: Save data
        """
        if saveOverride:
            saveObject = saveOverride
        else:
            saveObject = self.save

        savefile = open(file, "r+b")
        for location in self.__locations:
            if not key or location[2] == key:
                if location[2] == "deathcounter":
                    saveObject.deathcounter = random.randint(1, 200)
                if location[2] == "timestamp":
                    saveObject.timestamp = 0
                if location[2] == "elapsed":
                    saveObject.elapsed = 54000000
                if location[2] == "version":
                    saveObject.version = "6.9.6.9"
                # TODO - Add shrine support when ready
                savefile.seek(location[0])
                locationData = saveObject.get(location[2])
                locationData = locationData[:location[1]*2]
                for i in range(0, location[1]*2, 2):
                    hexData = int(locationData[i:i+2], 16)
                    byte = hexData.to_bytes(1, "little")
                    savefile.write(byte)
                if key:
                    break
        savefile.close()
        return saveObject

    def _unprotectedWrite(self, file, key: Optional[str] = None, saveOverride: Optional[Save] = None) -> Save:
        """
        Write the data to the given file and save the data. Unprotected version without restrictions.
        :param file: File to open and store data into
        :param key: Optional specific value to save
        :param saveOverride: Override for where to source the data
        :return: Save data
        """
        if saveOverride:
            saveObject = saveOverride
        else:
            saveObject = self.save

        savefile = open(file, "r+b")
        for location in self.__locations:
            if not key or location[2] == key:
                savefile.seek(location[0])
                locationData = saveObject.get(location[2])
                locationData = locationData[:location[1] * 2]
                for i in range(0, location[1] * 2, 2):
                    hexData = int(locationData[i:i + 2], 16)
                    byte = hexData.to_bytes(1, "little")
                    savefile.write(byte)
                if key:
                    break
        savefile.close()
        return saveObject

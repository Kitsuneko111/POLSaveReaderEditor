"""Python class for storing save information as an object"""
from typing import List, Union, Optional

from util.hexextendor import hexExtendor
from util.locations import locations


def convertFromHex(val: str, valtype: type) -> Union[int, str, list, TypeError]:
    """
    Convert a vlue from reverse hex to str/int
    :param val: Reverse Hex value
    :param valtype: What to convert to
    :return: Int or Str conversion of Reverse hex
    """
    if valtype == int:
        hexval = ""
        for i in range(len(val) - 2, -1, -2):
            hexval += val[i] + val[i + 1]
        return int(hexval, 16)
    elif valtype == str:
        newval = ""
        for i in range(0, len(val) - 1, 2):
            newval += chr(int(val[i] + val[i + 1], 16))
        return newval
    elif valtype == list:
        hexlist = [val[:4], val[4:8], val[8:12]]
        newval = [hexlist[i][2:4] + hexlist[i][:2] for i in range(3)]
        newval = [int(val, 16) for val in newval]
        return newval
    else:
        return TypeError("Invalid conversion target type: " + str(valtype))


def convertToHex(val: Union[int, str, list]) -> Union[str, TypeError]:
    """
    Convert a given int or str to the save file's reverse hex format
    :param val: Value to convert
    :return: Reversed Hex
    """
    if type(val) == int:
        hexval = hexExtendor(val)
        newhexval = ""
        for i in range(len(hexval) - 2, -1, -2):
            newhexval += hexval[i] + hexval[i + 1]
        return newhexval
    elif type(val) == str:
        try:
            return convertToHex(int(val))
        except ValueError:
            hexval = ""
            for char in val:
                hexval += hexExtendor(ord(char), 2)
            newhexval = ""
            for i in range(0, len(hexval) - 1, 2):
                newhexval += hexval[i] + hexval[i + 1]
            return newhexval
    elif type(val) == list:
        hexlist = [hexExtendor(listval, 4) for listval in val]
        vallist = [hexlist[i][2:4] + hexlist[i][:2] for i in range(3)]
        return "".join(vallist)

    else:
        return TypeError("Invalid conversion source type: " + str(type(val)))


class Save:
    """
    Class for the save data currently known in the game
    """

    def __init__(self):
        self.timestamp: Optional[int] = None
        self.version: Optional[str] = None
        self.elapsed: Optional[int] = None
        self.deathcounter: Optional[int] = None
        self.slot: Optional[int] = None
        """
        1. Village Intro
        3. A New Friend
        4. Getting to know each other
        5. The Cave
        6. The Highlands
        7. The Swamp
        9. The Shipwreck
        10. In Control
        12. Archipelago 1
        14. The Desert
        15. The Desert Hut
        16. The Robot Base
        17. Home
        """
        self.__chapters = (1, 3, 4, 5, 6, 7, 9, 10, 12, 14, 15, 16, 17)
        self.chapterId: Optional[int] = None
        self.sceneId: Optional[int] = None
        self.position: Optional[List[int]] = None

        self.__locations = locations

    def get(self, attr: Union[str, int]) -> Union[str, AttributeError, KeyError]:
        """
        Get values based on either address or value name
        :param attr: Attribute to get
        :return: Value | Error
        """
        if type(attr) == int:
            for location in self.__locations:
                if location[0] == attr:
                    return convertToHex(self.__getattribute__(location[2]))
            raise KeyError("No such save location currently known: " + str(attr))

        else:
            if attr[:2] == "__":
                raise AttributeError("Trying to access protected value: " + str(attr))
            attribute = self.__getattribute__(attr)
            if attribute is None:
                raise KeyError("Save value does not currently have a value: " + str(attr))
            else:
                return convertToHex(attribute)

    def set(self, key: Union[str, int], val: str) -> Union[None, KeyError, AttributeError]:
        """
        store values inside the class
        :param key: Key to store to
        :param val: Value to store
        :return: None | Error
        """
        if type(key) == int:
            for location in self.__locations:
                if location[0] == key:
                    val = convertFromHex(val, location[3])
                    self.__setattr__(location[2], val)
                    return
            raise KeyError("No such save location currently known: " + str(key))
        else:
            if key[:2] == "__":
                raise AttributeError("Trying to access protected value: " + str(key))
            for location in self.__locations:
                if location[2] == key:
                    val = convertFromHex(val, location[3])
                    self.__setattr__(key, val)
                    return
            raise KeyError("No such save value currently known: " + str(key))


if __name__ == "__main__":
    assert convertToHex(15) == "0f00000000000000", \
        "int convert to hex failure. Got " + str(convertToHex(15)) + " instead"
    assert convertFromHex("0f00000000000000", int) == 15, \
        "int convert from hex fail. Got " + str(convertFromHex("0f00000000000000", int)) + " instead"

    assert convertToHex("1.0.7.0") == "312e302e372e30", \
        "str convert to hex fail. Got " + str(convertToHex("1.0.7.0")) + " instead"
    assert convertFromHex("312e302e372e30", str) == "1.0.7.0", \
        "str convert from hex fail. Got " + str(convertFromHex("312e302e372e30", str)) + " instead"

    assert convertToHex([12, 13, 14]) == "0c000d000e00", \
        "list convert to hex fail. Got " + str(convertToHex([12, 13, 14])) + " instead"
    assert convertFromHex("0c000d000e00", list) == [12, 13, 14], \
        "list convert from hex fail. Got " + str(convertFromHex("0c000d000e00", list)) + " instead"

    saveFile = Save()
    saveFile.set("position", "0c000d000e00")
    assert saveFile.position == [12, 13, 14], \
        "Save file set fail. Got " + str(saveFile.position) + " instead"
    # Illegal access of private attribute to allow secure testing of hex value access
    assert saveFile.get(saveFile._Save__locations[-1][0]) == "0c000d000e00", \
        "Save file get fail. Got " + str(saveFile.get("position")) + " instead"

    print("All tests passed successfully")

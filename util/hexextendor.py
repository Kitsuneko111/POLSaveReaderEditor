"""
Util file including hex extending functions
"""


def hexExtendor(val, length=8):
    """
    Zfills a hex value with required bytes
    :param val: Value to convert to hex
    :param length: Optional length for the hex to be
    :return: Hex value
    """
    return hex(val)[2:].zfill(length)

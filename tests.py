"""
Test cases lololol
"""
from reader import Reader
from util.save import Save
from writer import Writer

save = Save()
reader = Reader(save)
writer = Writer(save)

reader.readFile("test.sav")
save.version = "6.9.6.9"
writer.writeFile("newtest.sav")
reader.readFile("newtest.sav")
assert save.version == "6.9.6.9",\
    "file overwrite or read error. Got "+str(save.version)+"instead"
assert save.timestamp == 0, \
    "file overwrite error, did not overwrite timestamp. Got "+str(save.timestamp)+" instead"
assert save.elapsed == 54000000, \
    "file overwrite error, did not overwrite elapsed. Got "+str(save.elapsed)+" instead"
assert save.deathcounter != 0, \
    "file overwrite error, did not change deaths. Got "+str(save.deathcounter)+" instead"
print("All tests passed successfully")

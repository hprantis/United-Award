import os

list_ = ["BOS to LAX on 2022-09-10", "BOS to LAX on 2022-09-10", "BOS to LAX on 2022-09-10"]
path = os.getcwd()
#exists = os.path.exists(path+r"\test.txt")
'''
if exists:
    file = open("test.txt", "r")
    var = file.read()
    file.close()

    file2 = open("test2.txt", "w")
    file2.write(var)
    file2.close()
else:
    file = open("test.txt", "w")
    file.close()

# reads the file first and saves it to the backup file,
# code below changes the new file without modifying backup

file = open("test.txt", "w")
for i in list_:
    file.write(i)
file.close()
'''
list1 = ["BOS to ABE on 2022-12-18", "BOS to AVP on 2022-12-18", "BOS to CHS on 2022-12-18", "BOS to LAX on 2022-12-18"]
list2 = ["PHL to BOS on 2022-12-23", "CHS to BOS on 2022-12-23", "EWR to BOS on 2022-12-23", "IAD to BOS on 2022-12-23"]

list3 = []
list4 = []

for i in list1:
    list3.append(i[7:10])

for i in list2:
    list4.append(i[:3])

for i in list3:
    if i in list4:
        print(i)

'''
From BOS to CHS
    departure dates:
        2022-08-20
        2022-08-22
        2022-08-23
    
    return dates:
        2022-08-22
        2022-08-23
        2022-08-25
        
for i in range(206+1):
    print("{:.2f}".format(i/206*100) + "%")
    #rint(i/206*100)
'''


def percent(counter, mode):
    if mode == 1:
        return "{:.2f}".format(counter/206*100) + "%"

mode = 1

for i in range(207):
    print(percent(i,"1"))



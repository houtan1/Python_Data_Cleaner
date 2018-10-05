# run with python helloworld.py
# print("hello world")

# tab delimited text dataset downloaded from https://doi.pangaea.de/10.1594/PANGAEA.885775 as Doering-etal_2018.tab
# let's read in that data
file = open("data/Doering-etal_2018.tab", "r")
line = file.readlines()
# print(line[28])
# print(len(line))

for x in range(29, len(line)):
    # print(line[x].split('\t'))
    # print(len(line[x].split('\t')))
    thisArray = line[x].split('\t')
    # print(len(thisArray))
    if thisArray[11] == "\n":
        print("Missing Age! Length(mm): " + thisArray[9] + " Diameter(mm): " + thisArray[10])

file.close()

# the above script opens the tab delimited data file in read format
# it then reads the data portion of the file, row by row
# the script searches for data rows which are missing the value for age
# it flags those rows and informs the user of their length and diameter values

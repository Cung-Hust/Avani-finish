a_file = open("data-test.txt", "r")
# get list of lines

lines = a_file.readlines()
a_file.close()

new_file = open("data-test.txt", "w")
for line in lines:
    if line.strip("\n") != "15:48:05:D0004503000000000000000000000000111":
# Delete "line2" from new_file

        new_file.write(line)

new_file.close()

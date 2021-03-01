a_file = open("data-test.txt", "r")

lines = a_file.readlines()
a_file.close()

del lines[0]


new_file = open("data-test.txt", "w+")

for line in lines:
    new_file.write(line)

new_file.close()

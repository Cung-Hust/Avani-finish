#!/usr/bin/python

# Mở file
file = open("plc.txt", "wb")
file.write("Python là ngôn ngữ tốt nhất".encode())

# Đóng file
file.close()
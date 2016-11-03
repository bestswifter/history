#!/usr/bin/python
# encoding: utf-8

import sys
import os

def history(pattern):
	home_path = os.popen("echo ~").read().strip('\n')
	file_name = home_path + "/.histfile"
	destination = home_path + "/.history/.histfile_func"
	command_color = "grep -n --color=always \"" + pattern + "\" " + file_name
	command_no_color = "grep -n --color=no \"" + pattern + "\" " + file_name

	result_color = os.popen(command_color).readlines()
	result_no_color = os.popen(command_no_color).readlines()
	new_list = []

	for index, line in enumerate(result_no_color):
		suffix = line[line.find(';') + 1:].strip('\n')
		command = "function " + str(index + 1) + "(){" + suffix + "}\n"
		new_list.append(command)

	open(destination, "w").writelines(new_list)

	for index, line in enumerate(result_color):
		output = line[line.find(';') + 1:].strip('\n')
		print(str(index + 1) + " " + output)

history(sys.argv[1])

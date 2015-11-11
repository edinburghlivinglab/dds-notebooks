import json

if __name__ == "__main__":
	data = open("edinburgh_tmp.txt",'rb').read()
	data_list = data.split(">,<")
	# d2 = json.loads("edinburgh_tmp.json")
	print data_list

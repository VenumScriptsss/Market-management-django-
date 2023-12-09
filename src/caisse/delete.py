import json

string = "{'me':'1', 'he':'2' }"
dict = string
arr = ['us','3']
loadDict = eval(dict)
loadDict.update({arr[0]:arr[1]})
print(loadDict)
import json

def makejsondata(objpath):
    with open(objpath, 'r') as f:
        database = json.load(f)
        return database


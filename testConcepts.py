# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:48:44 2019

@author: pruetj
"""

from pymongo import MongoClient


client = MongoClient()
db = client['test']

# Create collection called "posts"
posts = db.posts

post_1 = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
post_2 = {
    'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'
}
post_3 = {
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    'author': 'Bill'
}



result = posts.insert_many([post_1, post_2, post_3])


print('Multiple posts: {0}'.format(new_result.inserted_ids))








import json
from bson import json_util
from datetime import datetime

Well1 = {
    "Type": "Temperature",
    'TimeDict' : ['12'],
    "Val" : 55
    }

db = client['test']
testDict = db.testDict
result = testDict.insert_one(Well1)

testDict.update_one({'Type': 'Temperature',
                     'Val' : 55}, {'$push':{'TimeDict': '13'}})



json.dumps(testDict, default=json_util.default)
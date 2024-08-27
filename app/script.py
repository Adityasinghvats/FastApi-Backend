# Script to enter data into mongoDB
import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["courses"]
collection = db["courses"]


# Opening json as read and passing it to courses
with open("courses.json", "r") as f:
    courses = json.load(f)

# index with name
collection.create_index("name")

# rating for each course
for course in courses:
    course['rating'] = {'rating': 0, 'total': 0}

for course in courses:
    for chapter in course['chapters']:
        chapter['rating'] = {'total': 0, 'count': 0}

for course in courses:
    collection.insert_one(course)

client.close()
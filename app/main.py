import contextlib
import pymongo
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

app = FastAPI()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["courses"]


# To get all courses
@app.get('/courses')
def get_courses(sort_by: str = 'date', domain: str = None):
    # set the rating.total and rating.count to all the courses based on the sum of the chapters rating
    for course in db.courses.find():
        total = 0
        count = 0
        for chapter in course['chapters']:
            with contextlib.suppress(KeyError):
                total += chapter['rating']['total']
                count += chapter['rating']['count']
        db.courses.update_one({'_id': course['_id']}, {'$set': {'rating': {'total': total, 'count': count}}})

    if sort_by == 'date':
        sort_field = 'date'
        sort_order = -1

    elif sort_by == 'rating':
        sort_field = 'rating.total'
        sort_order = -1

    else:
        sort_field = 'name'
        sort_order = 1

    # Empty list of query
    query = {}
    if domain:
        query['domain'] = domain

    courses = db.courses.find(query, {'name': 1, 'date': 1, 'description': 1, 'domain': 1, 'rating': 1, '_id': 0}).sort(
        sort_field, sort_order)
    return list(courses)

    # http: // 127.0.0.1: 8000 / courses?sort_by = rating & domain = mathematics


#     To get based on domain in postman edit params


# Get Course by course_id
@app.get('/courses/{course_id}')
def get_course(course_id: str):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, 'chapters': 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    try:
        course['rating'] = course['rating']['total']
    except KeyError:
        course['rating'] = 'Course not rated yet'

    return course


@app.get('/courses/{course_id}/{chapter_id}')
def get_chapter(course_id: str, chapter_id: str):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, })
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    # This retrieves the chapters field from the course document.
    #  If the field does not exist, it defaults to an empty list.
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    return chapter


# http://127.0.0.1:8000/courses/66b893678f66039b61417400/0

@app.post('/courses/{course_id}/{chapter_id}')
# Rating field has a default value , lower value and higher value which is not included
def rate_chapter(course_id: str, chapter_id: str, rating: int = Query(..., gt=-1, lt=6)):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, })
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail="Chapter not found") from e
    try:
        chapter['rating']['total'] += rating
        chapter['rating']['count'] += 1
    # chapter['rating'] = {'total': rating, 'count': 1}:
    #  This line initializes the rating key with a dictionary containing
    #  the total rating set to the current rating and the count of ratings set to 1
    except KeyError:
        chapter['rating'] = {'total': rating, 'count': 1}
    db.courses.update_one({'_id': ObjectId(course_id)}, {'$set': {'chapters': chapters}})
    return chapter


@app.patch('/courses/{course_id}/{chapter_id}/{chapter_name}')
def change_chapter_name(course_id: str, chapter_id: str, chapter_name: str):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, })
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail="Chapter not found") from e
    try:
        chapter['name'] = chapter_name
    except KeyError:
        chapter['name'] = {'name': chapter_name}
    db.courses.update_one({'_id': ObjectId(course_id)}, {'$set': {'chapters': chapters}})
    return chapter

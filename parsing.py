# -*- coding: utf-8 -*-
from requests import get
import json
import datetime


def parsing_coursera():
    final_json = []
    json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)
    courses = get("https://api.coursera.org/api/courses.v1?q=search&query=web,веб&includes=instructorIds&fields=name,description,photoUrl,categories,primaryLanguages,instructorIds").json()["elements"]
    
    for elem in courses:
        final_json.append({
            'card': {
                'link': 'https://www.coursera.org/learn/' + elem['slug'],
                'title': elem['name'],
                'author': ', '.join(author['fullName'] for author in get('https://api.coursera.org/api/instructors.v1?ids=' + ','.join(elem['instructorIds'])).json()['elements']),
                'description': elem['description'],
                'date': datetime.datetime.now(),
                'image': elem['photoUrl'],
                'language': ','.join(elem['primaryLanguages']),
                'type': 'Video',
                'free': True,
                'tags': elem['categories'],
                'level': 1,
                'submittedBy': 'System',
                'vox': {
                    'favs': 0,
                    'votes': 0,
                    'views': 0
                }
            }
        })
    with open('data.json', 'w') as f:
        json.dump(final_json, f)
    



    
    
#for filling in questions/answers/votes
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'qna.settings'
import csv
from questions.models import *

newlist=[]
data=csv.reader(open('qna/qna_question_data.csv'))
for row in data:
  newlist.append(row)
for x in newlist:
  q, created=Question.objects.get_or_create(question=x[0])
  q.save()
  for y in x[1:]:
    a, created=Answer.objects.get_or_create(question_id=q.id, answer=y)
    a.save()
  q.save()
Answer.objects.filter(answer="").delete()

from core.models import *
from random import randint
import datetime

Vote.objects.all().delete()
for user in UserProfile.objects.all():
  for q in Question.objects.all():
    print user.votes.count()
    print q.answer_set.count()
    a = q.answer_set.all()[randint(0, q.answer_set.count()-1)]
    newvote=Vote.objects.create(answer_id=a.id)
    newvote.voter=user
    newvote.created=datetime.datetime(2013,randint(1,12),randint(1,28),randint(0,23),randint(0,59),randint(0,59))
    newvote.save()
    q.answered_by.add(user)
    a.selected_by.add(user)
    q.save()
    a.save()

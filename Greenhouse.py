import requests
import re
import json
import operator

import nltk
from nltk.corpus import stopwords

#The corpus
all_descriptions = ''
#Excludes non-English-language offices to avoid translation issues
ignore_offices = [6827,18842,18859,18855,18858]

#Remove HTML markup
clean_strings = ['&lt;p&gt;','&lt;div&gt;','&lt;/div&gt;''&lt;strong&gt;','&lt;/strong&gt;',u'\u2013','&lt;/li&gt;','&lt;/ul&gt;','&lt;ul&gt;','&lt;li&gt;','&lt;span&gt;','&lt;/span&gt;','&lt;br&gt;','&lt;/p&gt;','&lt;','&gt;','&;','quot','\u0026lt;li\u0026gt;','','\u0026lt;strong\u0026gt;','\u0026lt;','\u0026gt;','\u0026quot;','style','font','weight','400;','span','strong','BuzzFeed is the leading independent digital media and tech company delivering news and entertainment content to a global audience. We have offices in 19 cities around the world and more than 1500 employees including reporters, video producers, data scientists, engineers, brand strategists, and more. We fuse hard work and fun, through a culture of experimentation, teamwork, equality, and humble confidence. As an employee', 'enjoy perks like office events, snacks, career development courses, and no work on your birthday! But most importantly',u'\xa0',u'\u2014',u'\u2019',u'\u201d',u'\u201c','work with inspiring colleagues to build tools and create content that helps connect people all over the world.','=&;-:','&;','Requirements:','href','www','work','http','.com','amp;','To Apply For This Position:',u'\xa3',u'\u2026',u'\xe9',u'\xad','li ','is the leading independent digital media and tech company delivering news and entertainment content to a global audience. We have offices in 18 cities around the world and more than 1300 employees including reporters, video producers, data scientists, engineers, brand strategists, and more. We infuse hard work and fun though a culture of experimentation, teamwork, equality, and humble confidence. As an employee,','div/div',u'\u200b','Responsibilities:','/div','=-size: small;','youll','â€™']

#populate job IDs from job board
jobIds = []
getJobIds = "https://boards.greenhouse.io/embed/job_board?for=buzzfeed&b=https://www.buzzfeed.com/about/jobs"
got = requests.get(getJobIds)
jobIds = re.findall('jid=([0-9]+)',got.content)
print(jobIds)

#board token is company name, job id for buzzfeed is 6 digit sequence
for jobId in jobIds:
    uri = 'https://api.greenhouse.io/v1/boards/buzzfeed/jobs/' + jobId
    r = requests.get(uri)
    data = json.loads(r.content)
    descrip = data["content"]
    try:
        if json.loads(r.content)["offices"][0]["id"] not in ignore_offices:
            #Trash markup and stock phrases
            for s in clean_strings:
                descrip = descrip.replace(s,"")
            all_descriptions = all_descriptions + ' ' + descrip.decode("utf8")
    except:
        print('Error with listing no. ' + jobId)
        continue
    
    #You can save corpus for later
    f = open('Buzzfeed.txt','w')
    f.write(all_descriptions)
    f.close

current_word = {}
current_count = 0
response = open('Buzzfeed.txt','r')
each_word = []
count = 1
same_words ={}
word = []
#Collect all the words into a list
for line in response:
    line_words = line.split()
    for word in line_words:  # looping each line and extracting words
        each_word.append(word)

#Filters out English stop words
#Creates dict, increments mapping Value by 1 if key is in dict already
for words in each_word:
    if len(words) > 2 and words.lower() not in nltk.corpus.stopwords.words('english'):
        if words.lower() not in same_words.keys():
            same_words[words.lower()]=1
        else:
            same_words[words.lower()]=same_words[words.lower()]+1
        
same_words = sorted(same_words.items(), key=operator.itemgetter(1))
for each in same_words:
    print(each)

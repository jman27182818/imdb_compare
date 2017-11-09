# This program returns the list of actors who have been in the same
# two TV shows.  The inputs are the show names (this assumes that the
# titles you input would be the top resuld in an imdb search)



# standard system and regex calls
import sys
import re
from subprocess import call

from urllib.request import urlopen



print("Please type the name of the show with no spaces at the begining or end \n")
show1 = input("what is the first show title: ")
show2 = input("what is the second show title: ")


#html stuff
query1 = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='+show1.replace(' ','+')+'&s=all'
query2 = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='+show2.replace(' ','+')+'&s=all'


queryhtmldata1 = urlopen(query1).read()
queryhtmldata2 = urlopen(query2).read()

q = re.compile('="/title/tt[0-9]+?/')
ids1 = q.findall(str(queryhtmldata1))
ids2 = q.findall(str(queryhtmldata2))


show1id = ids1[1][9:-1]
show2id = ids2[1][9:-1]


url1 = 'http://www.imdb.com/title/' + show1id + '/fullcredits?ref_=tt_cl_sm#cast'
url2 = 'http://www.imdb.com/title/' + show2id + '/fullcredits?ref_=tt_cl_sm#cast'

htmldata1 = urlopen(url1).read()
htmldata2 = urlopen(url2).read()

print('\n')
p = re.compile('title="[^0-9]+?"')
actors1 = p.findall(str(htmldata1))
actors2 = p.findall(str(htmldata2))
# the common words in following "title=" for unwanted entries
wordlist = ['IMDB','Google', 'IMDb', 'Share ','image','Home']

def passes_filter(entry):
    for k in wordlist:
        if entry.find(k) >= 0:
            return False
    return True


def strip_title(text):
    return re.sub('title="', '', text)




actors1 = [strip_title(entry) for entry in actors1 if passes_filter(entry)]
actors2 = [strip_title(entry) for entry in actors2 if passes_filter(entry)]           

totalactors = actors1 + actors2


# showing duplicates
import collections
#TODO: use a better intersection algorithm
def intersec_basic(strA,strB,result):
    checker = 1
    for i in range(0,len(strA)):
        for j in range(0,len(strB)):
            if (strA[i] == strB[j]):
                checker = 0
        if checker ==0:
            result.append(strA[i])
        checker = 1

def intersec_sort1(strA,strB,result):
    strA.sort()
    strB.sort()
    i=0
    j=0

    while (i < len(strA) and j < len(strB)):
        if strA[i]<strB[j]:
            i += 1
        elif strA[i] > strB[j]:
            j += 1
        else:
            result.append(strA[i])
            i +=1
            j +=1

    
sameactors = []
intersec_sort1(actors1,actors2,sameactors)

#print sameactors
print("show 1 ID: "+show1id+"\n" + "show 2 ID: " + show2id +"\n")
print(sameactors)
print('number of actors in show 1: \n')
print(len(actors1))
print('number of actors in show 2: \n')
print(len(actors2))
print('number of same actors : \n')
print(len(sameactors))
print('\n')



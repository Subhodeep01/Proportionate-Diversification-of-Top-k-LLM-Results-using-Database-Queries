import pymysql

# Establish a connection to the local MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='exp'
)

#Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Query to retrieve data from database with given criteria:

# Query 1: find top-10 movies from genre {sci-fi, documentary, romance} average rating >8.0
# query = ["select ml.genre1, count(ml.genre1) from MovieList ml, ratings rt where ml.tconst = rt.tconst and ml.genre1 is not null and averageRating > 8.0 group by ml.genre1 having ml.genre1 in ('Romance', 'Documentary', 'Sci-Fi') order by ml.genre1;",
#          "select ml.genre1, count(ml.genre1) from MovieList ml, ratings rt where ml.tconst = rt.tconst and ml.genre1 is not null group by ml.genre1 having ml.genre1 in ('Romance', 'Documentary', 'Sci-Fi') order by ml.genre1;"]

# Query 2: find top-10 movies in language {English, French, Italian} with average rating >8.0
# query = ["select rg.lang, count(rg.lang) from regions rg, ratings rt where rg.titleid = rt.tconst and rg.lang is not null and averageRating > 9.5 group by rg.lang having rg.lang in ('en', 'fr', 'it') order by rg.lang;",
#          "select rg.lang, count(rg.lang) from regions rg, ratings rt where rg.titleid = rt.tconst and rg.lang is not null group by rg.lang having rg.lang in ('en', 'fr', 'it') order by rg.lang;"]

# Query 3: Find top-10 movies in English, Hebrew, and Cantonese/Yue Chinese that has low votes but high ratings.
query = ["select rg.lang, count(rg.lang) from regions rg, ratings rt where rg.titleid = rt.tconst and rg.lang is not null and averageRating > 8.0 and numVotes < 15000 group by rg.lang having rg.lang in ('en', 'he', 'yue') order by rg.lang;",
         "select rg.lang, count(rg.lang) from regions rg, ratings rt where rg.titleid = rt.tconst and rg.lang is not null group by rg.lang having rg.lang in ('en', 'he', 'yue') order by rg.lang;"]

#Query 4: Find top-10 movies in English, Hebrew, and Chinese that has high votes but low ratings.
# query = ["select rg.lang, count(rg.lang) from regions rg, ratings rt where rg.titleid = rt.tconst and rg.lang is not null and averageRating < 6.5 and numVotes > 150000 group by rg.lang having rg.lang in ('en', 'he', 'yue') order by rg.lang;",
#          "select rg.lang, count(rg.lang) from regions rg, ratings rt where rg.titleid = rt.tconst and rg.lang is not null group by rg.lang having rg.lang in ('en', 'he', 'yue') order by rg.lang;"]

#Query 5: find top-10 tv series from genre {sci-fi, documentary} average rating >8.0
# query = ["select ml.genre1, count(ml.genre1) from MovieList ml, ratings rt where ml.tconst = rt.tconst and ml.genre1 is not null and ml.titleType = 'tvSeries' and averageRating > 8.0 group by ml.genre1 having ml.genre1 in ('Documentary', 'Comedy') order by ml.genre1;",
#          "select ml.genre1, count(ml.genre1) from MovieList ml, ratings rt where ml.tconst = rt.tconst and ml.genre1 is not null and ml.titleType = 'tvSeries' group by ml.genre1 having ml.genre1 in ('Documentary', 'Comedy') order by ml.genre1;"]

data = []

# Execute the query
for que in query:
    cursor.execute(que)
    data.append(cursor.fetchall())


cursor.close()
conn.close()

# print(data)

dictionary = {}
i=0
for item in data[0]:
    # try:
    #     dictionary[item[0].replace("\r", "")] = [item[1], data[1][i][1]]
    # except:
    dictionary[item[0]] = [item[1], data[1][i][1]]
    i = i+1
# print(dictionary)

# dict2 = {}

# # Convert dictionary items to a list of tuples
# items = list(dictionary.items())
# remember_key = ""
# for current_item, next_item in zip(items, items[1:]):
#     current_key, current_value = current_item
#     next_key, next_value = next_item

#     # Perform operations on current item and next item
#     # Example operation: calculate the sum of current and next values
#     if current_key[0:3] == next_key[0:3]:
#         dict2[current_key] = [current_value[0]+next_value[0],current_value[1]+next_value[1]]
#     # elif current_key[0:3] != remember_key[0:3]:
#     #     dict2[current_key] = current_value
#     # remember_key = current_key
# # print(dict2)


#Calculating the proportion and appending it to the list of vals corresponding to each genre 

n = 10

def proportion(mydict):
    r = 0
    t=0
    j = 0
    for key,val in mydict.items():
        x = val[0]
        y = val[1]
        z = round(x/y,4)
        val.append(z)
        r = r + z
        j += 1
    # print(j)
    for key,val in mydict.items():
        val.append(int(round((val[2]/r)*n,0)))
        t = t + val[-1]
    return t 

# Eliminating the issue of the number of movies required, i.e, n == 10 == t (# of movies req) 
def maxkey(dictionary):
    temp = 0
    max_key =  None
    for keys, vals in dictionary.items():
        if vals[-2] > temp:
            max_key = keys
    return max_key

def minkey(dictionary):
    temp = 0
    min_key = None
    for keys, vals in dictionary.items():
        if vals[-2] > temp:
            min_key = keys
    return min_key

t = proportion(dictionary)

import copy
temp = 0
tempdict = copy.deepcopy(dictionary)
while(t < n):
    max_key = maxkey(tempdict)
    dictionary[max_key][-1] += 1
    t += 1
    del tempdict[max_key]

tempdict = copy.deepcopy(dictionary)
while(t>n):
    min_key = minkey(tempdict)
    dictionary[min_key][-1] += 1
    t -= 1
    del tempdict[min_key]
print(dictionary, t)


# Formatting the output obtained from MySQL into gpt-understandable text
mystring = ""

for key,vals in dictionary.items():
    # mystring += str(int(vals[-1])) + " of genre " + key + ", "               #for query 1
    mystring += str(int(vals[-1])) + " movies in language " + key + ", "     #for query 2, 3 and 4
    # mystring += str(int(vals[-1])) + " tv-series of genre " + key + ", "       #for query 5 

# input_data = f"List top {t} movies with {mystring}".rstrip(", ")              #for query 1, 2
input_data = f"List a total of {t} movies with {mystring}".rstrip(", ") + " with high ratings but low number of votes from audience"     #for query 3
# input_data = f"List a total of {t} movies with {mystring}".rstrip(", ") + " with low ratings but high number of votes from audience"     #for query 4
# input_data = f"List a top {t} tv-series with {mystring}".rstrip(", ")           #for query 5

print(input_data)

import openai

# Set your OpenAI API key
openai.api_key = ''
messages = []
messages.append({"role": "system", "content": "movies"})
messages.append({"role": "user", "content": input_data})
# Make a request to the GPT-3 API
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

# Get the generated response
reply = response["choices"][0]["message"]["content"]

# Process and display the generated response
print(reply)
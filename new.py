import imdb
import re
ia = imdb.IMDb()

##### code to modify given file
out = ""
with open('C:/Users/Saurabh Joshi/Desktop/ALDA/Netflix/movie_titles.csv') as test:
        for line in test:
            str = line.split(",")
            if(len(str)>3):
                temp = ""
                for i in range(2,len(str)):
                    temp = temp + str[i]
            else:
                temp = str[2]

            out += str[0] + "~" + str[1] + "~" + temp
with open('C:/Users/Saurabh Joshi/Desktop/ALDA/Netflix/movie_names.txt',"a") as file:
    file.write(out)

op = ""
with open('C:/Users/Saurabh Joshi/Desktop/ALDA/Netflix/movie_names.txt') as file:
    for line in file:
        j = line.split('~')
        r = ia.search_movie(j[2])
        for i in range(0, len(r)):
           # print(r[i].get('title'),j[2],j[1],r[i].get('year'))
            if j[2].strip() == str(r[i].get('title')).strip() and j[1].strip()== str(r[i].get('year')).strip():
                print(j[0])
                d = ""
                g = ""
                id = r[i].getID()
                str(id)
                movie = ia.get_movie(id)
                if movie.has_key('director'):
                    for director in movie['director']:
                        d = director['name']
                if movie.has_key('genres'):
                    for genre in movie['genres']:
                        g = g + genre + ":"
                    g = g[:-1]
                op = op + str(j[0])+","+str(r[i].get('title')) + "," + str(r[i].get('year')) + "," + str(r[i].get('kind')) + "," + d + "," + g.strip() + '\n'

with open('C:/Users/Saurabh Joshi/Desktop/ALDA/Netflix/movie_data.csv',"a") as file:
    file.write(op)





import pandas as pd
from flask import Flask, render_template, request
import pickle as pkl

with open('model.pkl','rb') as sim: 
    similarity=pkl.load(sim)

final_df=pd.read_csv('final_df.csv')
import difflib
list_of_all_titles = final_df['title'].tolist()
def name_match(n):
    find_close_match = difflib.get_close_matches(n, list_of_all_titles)
    close_match=find_close_match[0]
    index_of_the_movie = final_df[final_df.title == close_match].index.values[0]
    return index_of_the_movie

def suggester(n):
    similarity_score = list(enumerate(similarity[n]))
    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 
    arr=[]
    i=1
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index =final_df[final_df.index==index]['title'].values[0]
        if (i<30):
            arr.append(title_from_index)
            i+=1
    return arr




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.form['movie_name']

        return render_template('/recomendation.html', movie_name=movie_name)
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True)
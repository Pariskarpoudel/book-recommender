from flask import Flask, render_template,request
import pickle
import numpy as np
import pandas as pd 

final_df = pickle.load(open('final_df.pkl','rb'))
books = pickle.load(open('books_list.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend',methods=['POST'])
def recommend(): 
    book = str(request.form.get('user_input'))
    items=[]

    book_index = books.index(book)
    similarities = similarity_scores[book_index]
    movies_list_indices = np.argsort(similarities)[::-1][1:5]

    for index in movies_list_indices:
        title = final_df[final_df['Book-Title'] == books[index]].iloc[0].loc['Book-Title']
        author = final_df[final_df['Book-Title'] == books[index]].iloc[0].loc['Book-Author']
        imageurl = final_df[final_df['Book-Title'] == books[index]].iloc[0].loc['Image-URL-M']
        book_ = {"title":title,"author":author,"imageurl":imageurl} 
        items.append(book_) 
    return render_template('index.html',items=items)
if __name__ == '__main__':
    app.run(debug=True)
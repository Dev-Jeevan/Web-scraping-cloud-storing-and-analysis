from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import pymongo
from pymongo import MongoClient
app = Flask(__name__)
from bson.objectid import ObjectId

cluster = MongoClient("mongodb+srv://testuser:testuser123@cluster0.dj0nr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db  = cluster["testDb"]
collection = db["testData"]



# View
@app.route('/')
def index(methods=['POST','GET']):
    movies = collection.find()         
    return render_template('view.html',movies=movies)

# Create
@app.route('/add')
def add():
   return render_template('add.html')


# Delete
@app.route('/delete')
def delete():
   # collection.drop()
    myquery = { "name": "Amy" }
    collection.delete_one(myquery)
    return render_template('view.html')

# Delete Movie
@app.route('/delete_movie/<string:id>', methods=['POST','GET'])
def delete_movie(id):
    print(id)
    myquery = { "_id": ObjectId(id) }
    print(myquery)
    collection.delete_one(myquery)
   # flash('Movie Deleted', 'success')
   # return render_template('view.html')
   #print the customers collection after the deletion:
    for x in collection.find():
        print(x)
    return redirect(url_for('index'))

# Add Movie
@app.route('/add_movie', methods=['POST','GET'])
def add_movie():
    items = collection.find().count()
    print(items)
    FilmTitle = request.form.get('FilmTitle')
    IMDBRating = request.form.get('IMDBRating')
    RunTime = request.form.get('RunTime')
    Genre = request.form.get('Genre')
    ShortNarration = request.form.get('ShortNarration')
    Director = request.form.get('Director')
    mylist = [
        { "Film Title": FilmTitle,"IMDB Rating":IMDBRating,"Run Time":RunTime,"Genre":Genre,"Short Narration":ShortNarration,"Director":Director}
       
            ]
    collection.insert_many(mylist)
    return redirect(url_for('index'))
#Edit Movie
@app.route('/edit_movie/<string:id>', methods=['POST','GET'])
def edit_movie(id):
    print(id)
    myquery = { "_id": id }
    print(myquery)
    #movie = []
    documents= collection.find()
    for document in documents:
        if document['_id'] == ObjectId(id):
            #movie.append(document)
            movie=document
    print(movie)
    return render_template('edit.html',movie=movie)

    # Update
@app.route('/edit/<string:id>', methods=['POST','GET'])
def edit(id):
    ident=id
    FilmTitle = request.form.get('FilmTitle')
    IMDBRating = request.form.get('IMDBRating')
    RunTime = request.form.get('RunTime')
    Genre = request.form.get('Genre')
    ShortNarration = request.form.get('ShortNarration')
    Director = request.form.get('Director')
    myquery = { "_id": ObjectId(ident)} 
    print(myquery)
    newvalues = { "$set": { "Film Title": FilmTitle,"IMDB Rating":IMDBRating,"Run Time":RunTime,"Genre":Genre,"Short Narration":ShortNarration,"Director":Director }}
    print(newvalues)
    collection.update_one(myquery, newvalues)
    return redirect(url_for('index'))

   
   
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
from .models import Destination, Comment
from .forms import DestinationForm
from .forms import CommentForm
from . import db
destbp = Blueprint('destination', __name__, url_prefix='/destinations')


def get_destinations():

    # Brazil information
    brazil_description = "Nice Country"
    brazil_image = "task1_startpoint/travel/BrazilImage.png"
    destination = Destination('Brazil', brazil_description, brazil_image, 'R$10')


    # Comments
    comment = Comment("Kieran", "Was cool, no cart though", '2024-09-05 16:55:05')
    destination.set_comments(comment)

    comment = Comment("Ben", "Coffee was nice, might visit again", '2024-09-06 11:34:08')
    destination.set_comments(comment)

    comment = Comment("Andrew", "Nice place, nice sun, cool t-pose man", '2024-09-11 17:20:43')
    destination.set_comments(comment)


    
    return destination



@destbp.route('/<id>')
def show(id):
    #destination = get_destinations()
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    comment_form = CommentForm()
    return render_template('destinations/show.html', destination=destination, form=comment_form)

@destbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    # here the form is created  form = CommentForm()
    form = CommentForm()
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    
    if form.validate_on_submit():	#this is true only in case of POST method
        # read the comment from the form, associate the Comment's destination field
      # with the destination object from the above DB query
      comment = Comment(text=form.text.data, destination=destination, user=current_user) 
      # here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      # flashing a message which needs to be handled by the html
      # flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=Destination.id))

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = DestinationForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        
        # Create the destination
        destination = Destination(name=form.name.data, 
                                  description=form.description.data,
                                  image = db_file_path,
                                  currency=form.currency.data)
        
        
        # add to db.session
        db.session.add(destination)

        # commit it
        db.session.commit()
        print('Successfully created new travel destination')
        
        return redirect(url_for('destination.create'))
    return render_template('destinations/create.html', form=form)


def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path
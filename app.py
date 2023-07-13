from flask import Flask, request, render_template, redirect, flash, session, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import NewUserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_exercise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'chickenzarecool21837'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.app_context().push()
connect_db(app)
db.create_all()

@app.route('/')
def redirect_to_register():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def show_or_handle_registration():

    form = NewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data    
        newUser = User.registration(username, password, email, first_name, last_name)
        db.session.add(newUser)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please try another one.')
            return render_template('registration.html')
        session['username'] = newUser.username
        flash(f"Welcome, {newUser.username}!","success")
        return redirect(f'/users/{newUser.username}')
    
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET','POST'])
def show_or_handle_login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authorization(username, password)

        if user:
            session['username'] = user.username
            flash(f"Welcome back {user.username}","success")
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Incorrect username/password.']
    
    return render_template('login.html', form=form)

@app.route('/secret')
def show_secrets():
    if 'username' not in session:
        flash("You must be logged in to view","danger")
        return redirect('/')
    
    else:
        return render_template('secret.html')

@app.route('/logout')
def log_user_out():
    session.pop('username')
    flash("Goodbye!","info")
    return redirect('/')

@app.route('/users/<username>')
def show_user_details(username):
    if 'username' not in session:
        flash('Please log in first!',"danger")
        return redirect('/')
    else:
        user = User.query.get_or_404(username)
        return render_template('user_details.html', user=user)

        
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if session['username'] == username:
        user = User.query.get_or_404(username).delete()
        db.session.commit()
        session.pop('username')
        return redirect('/')
    else:
      abort(401)
    

    
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_or_handle_feedback_form(username):
    """Show or handle feedback form only for the signed-in user"""
    
    if 'username' not in session:
        flash('Must be signed in to provide feedback', 'danger')
        return redirect('/')
    
    if username != session['username']:
        abort(401)

    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()

        flash('Thank you for the feedback!', 'success')
        return redirect(f'/users/{username}')
        
    return render_template('/feedback_form.html', form=form)

        
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def show_or_handle_feedback_update_form(feedback_id):
    """Show or handle feedback update form only for signed in user"""
    
    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user

    if 'username' not in session or user.username != session['username']:
            flash('Must be signed in to update feedback','danger')
            return redirect('/')
    else:       
            form = FeedbackForm(obj = feedback)

            if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data
                db.session.commit()

                flash('Feedback updated!','success')
                return redirect(f'/users/{user.username}')
        
            else:
                return render_template('/feedback_update_form.html',form=form)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feeback(feedback_id):
    """Delete feedback if user logged in"""
    
    if 'username' not in session:
         flash('Must be logged in to delete/update feedback','danger')
         return redirect('/')
    
    else:
        feedback = Feedback.query.get_or_404(feedback_id)
        user = feedback.user

        if session['username'] == user.username:
             db.session.delete(feedback)
             db.session.commit()
             flash('Feedback deleted.','success')
             return redirect(f'/users/{user.username}')
        
        else:
            abort(401)
         
        
@app.errorhandler(404)
@app.errorhandler(401)
def page_not_found(e):
    # Render template for custom error message
    return render_template(f'{e.code}.html'), e.code

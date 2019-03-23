from flask import Flask,render_template,url_for,flash,redirect,request,abort
from ajaira import app,db,bcrypt,login_manager
from ajaira.form import RegistrationForm,LoginForm,UpdateForm,PostForm
from ajaira.models import User,Post,Vote,Fighter,Voter
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image
from sqlalchemy import func

active=True


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,"static/img",picture_fn)
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/comment",methods=["GET","POST"])
@login_required
def comment():
    form=PostForm()
    com=Post(comment=form.title.data,author=current_user)
    db.session.add(com)
    db.session.commit()
    return redirect("home")



@app.route("/")
@app.route("/home",methods=["GET","POST"])
@login_required
def home():
    form=PostForm()

    posts=Post.query.order_by(Post.date_posted.desc()).all()
    image_file = url_for('static', filename='img/' + current_user.image_file)

    if form.validate_on_submit():



            if form.image.data:
                picture_img=save_image(form.image.data)

                post=Post(caption=form.title.data,content=form.content.data,image=picture_img,author=current_user)

            else:
                post=Post(caption=form.title.data,content=form.content.data,author=current_user)

            db.session.add(post)
            db.session.commit()
            flash("YOur post has been created!","success")
            return redirect(url_for('home'))

    return render_template("home.html",posts=posts,active=active,image_file=image_file,form=form,legend="New Post")




@app.route("/blog",methods=["GET","POST"])
@login_required
def blog():
    form=PostForm()
    posts=Post.query.order_by(Post.date_posted.desc()).all()
    image_file = url_for('static', filename='img/' + current_user.image_file)
    if form.validate_on_submit():

            if form.image.data:
                picture_img=save_image(form.image.data)

                post=Post(title=form.title.data,content=form.content.data,image=picture_img,author=current_user)
            else:
                post=Post(title=form.title.data,content=form.content.data,author=current_user)
            db.session.add(post)
            db.session.commit()
            flash("YOur post has been created!","success")
            return redirect(url_for('blog'))

    return render_template("blog.html",active=active,form=form,posts=posts,image_file=image_file)
@app.route("/post/<int:post_id>/update_blog",methods=["GET","POST"])
@login_required
def update_blog(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("Your blog has been update!","success")
        return redirect(url_for('blog_single',post_id=post.id))
    elif request.method=="GET":
        form.title.data=post.caption
        form.content=post.content
    return render_template('blog.html',post=post,form=form,legend="Update post",active=active)


@app.route("/post/<int:post_id>/delete_blog",methods=["POST"])
@login_required
def delete_blog(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("YOur Blog post has delete successfully","success")
    return redirect("blog")


@app.route("/people")
@login_required
def people():

    user=User.query.all()
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template("people.html",active=active,user=user,image_file=image_file)


def fighter_set():
    rahi= Fighter(name='Rahi')
    sharuk = Fighter(name='Sharuk')

    # add fighters to session
    db.session.add(rahi)
    db.session.add(sharuk)

    # commit the fighters to database
    db.session.commit()

@app.route("/contest",methods=["GET","POST"])
@login_required
def contest():
    message = None
    message_level = ''
    if request.method == 'POST':
        email =current_user.email #request.form.get('email')
        fighter_id = request.form.get('fighter')
        if email and fighter_id:
            voter = db.session.query(Voter).filter_by(email=email).first()
            if voter:
                message_level = 'info'
                message = 'You have already voted!'
            else:
                user = User.query.filter_by(email=email).first()


                fighter = db.session.query(Fighter).filter_by(id=fighter_id).first()
                vote = Vote(user=user,fighter=fighter)
                db.session.add(vote)

                voter_fcheck=Voter(email=vote.user.email)
                db.session.add(voter_fcheck)
                db.session.commit()
                message_level = 'success'
                message = 'Your vote for {} has been submitted!'.format(fighter.name)
        #else:
        #    message_level = 'danger'
        #    message = 'You must enter your email and select a fighter to cast a vote.'

    fighters = Fighter.query.order_by('id').all()
    total_votes = db.session.query(Vote).count()
    vote_query = db.session.query(Vote.fighter_id, func.count(Vote.fighter_id))
    vote_counts = vote_query.group_by(Vote.fighter_id).order_by('fighter_id').all()

    return render_template('contest.html', message=message, message_level=message_level,
                           fighters=fighters, total_votes=total_votes, vote_counts=vote_counts)













@app.route("/profile/<string:username>/<int:id>")
@login_required
def profile(username,id):
    form = PostForm()

    user=User.query.filter_by(username=username).first_or_404()
    id=User.query.get(id)
    posts=Post.query.filter_by(author=id).order_by(Post.date_posted.desc()).all()
    user_img = url_for('static', filename='img/' + user.image_file)

    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('profile.html',user=user,id=id,posts=posts,image_file=image_file, form=form,active=active)

@app.route("/profile_edit", methods=['GET', 'POST'])
@login_required


def profile_edit():
    form = UpdateForm()


    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile',username=current_user.username,id=current_user.id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('profile_edit.html', title='Account', image_file=image_file, form=form,active=active)




def save_image(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext=os.path.splitext(form_picture.filename)
    #picture_fn="{{url_for('profile',username="+current_user.username+",id="+str(current_user.id)+")}}"
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,"static/img",picture_fn)
    form_picture.save(picture_path)

    return picture_fn




@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    loginform=LoginForm()
    if loginform.validate_on_submit():
        user=User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password,loginform.password.data):
            login_user(user,remember=loginform.remember.data)
            flash("Hello %s you login has successfull"%(user.username),"success")
            next_page=request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash("Please check your email and password.And Try Again!","danger")
    return render_template("login.html",loginform=loginform)



@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    registrationform=RegistrationForm()
    if registrationform.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(registrationform.password.data).decode('utf-8')
        user=User(username=registrationform.username.data,email=registrationform.email.data,password=hash_password)
        db.session.add(user)
        db.session.commit()

        flash("Account successfully create for %s now you may login "%(registrationform.username.data),"success")
        return redirect(url_for('login'))
    return render_template("register.html",registrationform=registrationform)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/post/<int:post_id>")
def post(post_id):
    form=PostForm()
    post=Post.query.get_or_404(post_id)


    return render_template('post_single.html',post=post,form=form,active=active)

@app.route("/blog_single/<int:post_id>")
def blog_single(post_id):
    form=PostForm()
    post=Post.query.get_or_404(post_id)

    return render_template('blog_single.html',post=post,form=form,active=active)

@app.route("/post/<int:post_id>/update_post",methods=["GET","POST"])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.caption=form.title.data
        db.session.commit()
        flash("Your post has been update!","success")
        return redirect(url_for('post',post_id=post.id))
    elif request.method=="GET":
        form.title.data=post.caption
    return render_template('post_single.html',post=post,form=form,legend="Update post",active=active)



@app.route("/post/<int:post_id>/delete_post",methods=["POST"])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("YOur post has delete successfully","success")
    return redirect("home")


@app.route("/user/<string:username>")
@login_required
def user_posts(username):
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    user_img = url_for('static', filename='img/' + user.image_file)
    image_file = url_for('static', filename='img/' + current_user.image_file)

    return render_template("user_posts.html",user=user,posts=posts,active=active,image_file=image_file,user_img=user_img)


@app.route("/chat")
@login_required
def chat():
    return render_template('chat.html',active=active)

@app.route("/pip")
def pip():
    return render_template('status.html',active=active)

@app.route("/game")
def game():


    return render_template("game.html",active=active)

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, Project
from app.forms import ProjectForm

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ProjectForm()
    
    # Eğer giriş yapılmışsa ve form doldurulup gönderildiyse veritabanına kaydet[cite: 1]
    if current_user.is_authenticated and form.validate_on_submit():
        project = Project(title=form.title.data, body=form.body.data, technologies=form.technologies.data, author=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Harika! Yeni proje başarıyla eklendi.')
        return redirect(url_for('index'))
        
    page = request.args.get('page', 1, type=int)
    query = sa.select(Project).order_by(Project.timestamp.desc())
    projects = db.paginate(query, page=page, per_page=app.config['PROJECTS_PER_PAGE'], error_out=False)
    
    next_url = url_for('index', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('index', page=projects.prev_num) if projects.has_prev else None
    
    # Formu şablona gönderiyoruz[cite: 1]
    return render_template('index.html', title='Ana Sayfa', form=form, projects=projects.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Giriş Yap', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Kayıt Ol', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is None:
        flash(f'Kullanıcı bulunamadı.')
        return redirect(url_for('index'))
    query = sa.select(Project).where(Project.author == user).order_by(Project.timestamp.desc())
    projects = db.session.scalars(query).all()
    return render_template('user.html', user=user, projects=projects)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Profil güncellendi.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Profili Düzenle', form=form)
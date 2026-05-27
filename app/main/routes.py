from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from flask_babel import _
from app.main import bp
from app.main.forms import EditProfileForm, ProjectForm
from app.models import User, Project

# Eskiden @app.before_request idi. Artık tüm modülleri kapsaması için @bp.before_app_request kullanıyoruz.
@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = ProjectForm()
    
    # Eğer giriş yapılmışsa ve form doldurulup gönderildiyse veritabanına kaydet
    if current_user.is_authenticated and form.validate_on_submit():
        project = Project(title=form.title.data, body=form.body.data, technologies=form.technologies.data, author=current_user)
        db.session.add(project)
        db.session.commit()
        flash(_('Harika! Yeni proje başarıyla eklendi.'))
        return redirect(url_for('main.index'))
        
    page = request.args.get('page', 1, type=int)
    query = sa.select(Project).order_by(Project.timestamp.desc())
    # current_app kullanıyoruz çünkü app artık global bir değişken değil
    projects = db.paginate(query, page=page, per_page=current_app.config['PROJECTS_PER_PAGE'], error_out=False)
    
    next_url = url_for('main.index', page=projects.next_num) if projects.has_next else None
    prev_url = url_for('main.index', page=projects.prev_num) if projects.has_prev else None
    
    return render_template('index.html', title=_('Ana Sayfa'), form=form, projects=projects.items, next_url=next_url, prev_url=prev_url)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is None:
        flash(_('Kullanıcı bulunamadı.'))
        return redirect(url_for('main.index'))
    query = sa.select(Project).where(Project.author == user).order_by(Project.timestamp.desc())
    projects = db.session.scalars(query).all()
    return render_template('user.html', user=user, projects=projects)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Profil güncellendi.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Profili Düzenle'), form=form)
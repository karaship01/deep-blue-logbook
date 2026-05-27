from time import time
import jwt
from datetime import datetime, timezone
from typing import Optional
from flask import current_app
import sqlalchemy as sa
import sqlalchemy.orm as so
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))

    projects: so.WriteOnlyMapped['Project'] = so.relationship(back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
        
    def get_reset_password_token(self, expires_in=600):
        # app.config yerine current_app.config kullanıldı (Circular Import Çözümü)
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            # app.config yerine current_app.config kullanıldı
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.get(User, id)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100))
    body: so.Mapped[str] = so.mapped_column(sa.String(500))
    technologies: so.Mapped[str] = so.mapped_column(sa.String(100))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='projects')
    
    # Yeni eklenen Comment modeli ile olan ilişki (One-to-Many)
    comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='project')


# --- HOCANIN ZORUNLU TUTTUĞU 3. MODEL EKLENDİ ---
class Comment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    project_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Project.id), index=True)

    project: so.Mapped[Project] = so.relationship(back_populates='comments')
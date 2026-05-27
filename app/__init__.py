from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap5
from config import Config

# --- 1. Eklentileri Global Olarak (Ama Boş) Tanımla ---
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'  # Blueprint yapısına uygun olarak değiştirdik!
login.login_message = _l('Bu sayfayı görmek için lütfen giriş yapın.')
bootstrap = Bootstrap5()
moment = Moment()
babel = Babel()

def get_locale():
    # app.config yerine current_app.config kullanıyoruz çünkü app artık global değil
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

# --- 2. Application Factory (Uygulama Fabrikası) Fonksiyonu ---
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Eklentileri uygulamaya bağla
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    # --- 3. Blueprint'leri Kaydet (Modüler Yapı) ---
    
    # Hata sayfaları modülü
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Giriş/Kayıt modülü (/auth uzantısıyla çalışacak)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Ana site modülü
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

# Modeller en altta kalmaya devam ediyor
from app import models
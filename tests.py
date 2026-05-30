import unittest
from app import create_app, db
from app.models import User

class UserModelCase(unittest.TestCase):
    def setUp(self):
        # Testler için izole bir ortam (memory) yaratıyoruz
        self.app = create_app()
        self.app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Test bittikten sonra veritabanını temizliyoruz
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        # Hocanın rubrikte istediği "Şifre hashleme" olayını test ediyoruz!
        u = User(username='test_dalgic', email='dalgic@example.com')
        u.set_password('derin_mavi_123')
        
        # Yanlış şifrenin reddedilmesi test ediliyor
        self.assertFalse(u.check_password('yanlis_sifre'))
        # Doğru şifrenin onaylanması test ediliyor
        self.assertTrue(u.check_password('derin_mavi_123'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
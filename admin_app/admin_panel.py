from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_admin import AdminIndexView, expose, Admin

from admin_app.admin_views import UserModelView
from configuration.core.config import base_config
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

from models import User
from services.auth_handler import AuthHandler

auth_handler = AuthHandler()

flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = base_config.SECRET
flask_app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{base_config.DB_USER}:{base_config.DB_PASS}@"
    f"{base_config.DB_HOST}:{base_config.DB_PORT}/{base_config.DB_NAME}"
)

flask_db = SQLAlchemy()
flask_db.init_app(flask_app)

flask_app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

login_manager = LoginManager()
login_manager.init_app(flask_app)


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return super(CustomAdminIndexView, self).index()


admin = Admin(flask_app,
              name="Admin",
              url="",
              index_view=CustomAdminIndexView(url=""),
              base_template="admin/master-extended.html")


admin.add_view(UserModelView(User, flask_db.session))


@login_manager.user_loader
def load_user(user_id):
    user = flask_db.session.query(User).filter(User.id == user_id).first()
    return user


@flask_app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = flask_db.session.query(User).filter(User.login == username).first()
        except Exception:
            flask_db.session.rollback()
            flask_db.session.close()
            return redirect(url_for('login'))
        else:
            if not user:
                return render_template('login_page.html')
            auth = auth_handler.verify_password(password, username, user.password)
            if user and auth and user.role == 'admin':
                try:
                    login_user(user)
                    url = url_for('admin.index')
                    return redirect(url)
                except Exception as e:
                    print("Error", e)
            else:
                return render_template('login_page.html')
    try:
        return render_template('login_page.html')
    except Exception as e:
        print("Error", e)


@flask_app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

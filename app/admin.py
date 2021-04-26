import flask_admin
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import url_for, redirect
from werkzeug.utils import secure_filename
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from app import models, app, db
import os


def prefix_name(obj, file_data):
    parts = os.path.splitext(file_data.filename)
    return app.config['STORAGE'] + '/' + secure_filename('file-%s%s' % parts)


class CustomModelView(ModelView):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class PostModelView(CustomModelView):
    form_extra_fields = {
        'image_path': form.ImageUploadField('image_path', base_path='app/static/', namegen=prefix_name)
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']

    form_overrides = {
        'body': CKTextAreaField
    }


admin = flask_admin.Admin(app, template_mode='bootstrap4')
admin.add_view(CustomModelView(models.User, db.session))
admin.add_view(PostModelView(models.Post, db.session))

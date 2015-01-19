from flask import render_template, flash, redirect, url_for, abort,\
    request, current_app
from flask.ext.login import login_required, current_user
from ..models import User, Talk
from . import talks
from .forms import ProfileForm, TalkForm, CommentForm, PresenterCommentForm


@talks.route('/')
def index():
    talks = Talk.all();
    return render_template('talks/index.html', talks=talks)


@talks.route('/user/<username>')
def user(username):
    user = User()
    return render_template('talks/user.html', user=user)


@talks.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        flash('Your profile has been updated.')
        return redirect(url_for('talks.user', username=current_user.username))
    form.name.data = current_user.name
    return render_template('talks/profile.html', form=form)


@talks.route('/new', methods=['GET', 'POST'])
@login_required
def new_talk():
    form = TalkForm()
    if form.validate_on_submit():
        talk = Talk()
        form.to_model(talk)
        flash('The talk was added successfully.')
        return redirect(url_for('.index'))
    return render_template('talks/edit_talk.html', form=form)


@talks.route('/talk/<id>', methods=['GET', 'POST'])
def talk(id):
    talk = Talk.load(id) 
    return render_template('talks/talk.html', talk=talk)


@talks.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_talk(id):
    talk = Talk.load(id)
    form = TalkForm()
    if form.validate_on_submit():
        form.to_model(talk)
        flash('The talk was updated successfully.')
        return redirect(url_for('.talk', id=talk.id))
    form.from_model(talk)
    return render_template('talks/edit_talk.html', form=form)



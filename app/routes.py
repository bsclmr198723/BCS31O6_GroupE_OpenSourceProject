from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegisterForm, RepositoryForm, EditRepositoryForm, IssueForm
from app.models import UserModel, RepositoryModel, IssueModel, Status, Category
from flask_login import current_user, login_user, logout_user, login_required, current_user

@app.route('/')
@login_required
def home():
    repos = RepositoryModel.query.filter_by(user=current_user)
    return render_template('main/home.html', title='Home', repos=repos)

@app.route('/register/',  methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = UserModel(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/login/',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('auth/login.html', title='Login', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create/repository/', methods=['GET', 'POST'])
@login_required
def create_repo():
    form = RepositoryForm()
    if form.validate_on_submit():
        new_repository = RepositoryModel(name=form.name.data, user=current_user, description=form.description.data)
        db.session.add(new_repository)
        db.session.commit()
        flash('Repository created successfully', 'success')
        return redirect(url_for('home'))
    return render_template('main/create_repo.html', form=form, title="Create Repo")

@app.route('/repository/<int:repo_id>/details/')
@login_required
def repo_detail(repo_id):
    repo = RepositoryModel.query.get(repo_id)
    issues = IssueModel.query.filter_by(repository_id=repo_id)
    return render_template('main/repo_details.html', repo=repo, issues=issues, title="Repo Details")

@app.route('/repository/<int:repo_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_repo(repo_id):
    repo = RepositoryModel.query.get(repo_id)

    form = EditRepositoryForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_name = form.name.data
        new_description = form.description.data
        repo.name = new_name
        repo.description = new_description
        db.session.commit()

        flash('Repository update successfully')
        return redirect(url_for('repo_detail', repo_id=repo.id))  
    
    form.name.data = repo.name
    form.description.data = repo.description
    
    return render_template('main/edit_details.html', repo=repo, form=form, title="Repo Details")

@app.route('/repository/<string:repo_id>/create_issue/', methods=['GET', 'POST'])
@login_required
def create_issue(repo_id):
    repo = RepositoryModel.query.get(repo_id)
    form = IssueForm()  

    form.status.choices = [(status.id, status.title) for status in Status.query.all()]
    form.category.choices = [(category.id, category.title) for category in Category.query.all()]

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        status_id = form.status.data
        category_id = form.category.data
        description = form.description.data
        created_by = current_user
        

        status = Status.query.get(status_id)
        category = Category.query.get(category_id)

        issue = IssueModel(
            title=title,
            status=status,
            category=category,
            description=description,
            created_by=created_by,
            repository_id=repo_id
        )

        db.session.add(issue)
        db.session.commit()

        flash('Issue created successfully')
        return redirect(url_for('create_issue', repo_id=repo_id))

    return render_template( 'main/create_issue.html', repo=repo, form=form, title="Issue")

# create issue list logic

@login_required
@app.route('/<string:repo_id>/issues/')
def issues_list(repo_id):
    template = 'main/issues_list.html'
    issues = IssueModel.query.filter_by(repository_id=repo_id).order_by(IssueModel.created_at.desc())
    repository = RepositoryModel.query.get(repo_id)
    return render_template(template, title="Issues", issues=issues, repository=repository)

# @login_required
# @app.route('/issues/<int:issue_id>/', methods=['GET', 'POST'])
# def issues_detail(issue_id):
#     template = 'core/issues_detail.html'
#     issue = IssueModel.query.get(issue_id)
#     comments = Comment.query.filter_by(issue_id=issue_id)

#     form = CommentForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         text = form.text.data

#         comment = Comment(issue_id=issue_id, user_id=current_user.id, text=text)
#         db.session.add(comment)
#         db.session.commit()





# Main file for blog


# Import statements
from flask import (
    Flask,
    render_template,
    redirect,
    Markup,
    request,
    flash,
    url_for,
    session
)
from db_functions import (
    get_posts,
    get_post,
    add_post,
    update_post,
    delete_post,
)
import markdown

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"
app.config["USERNAME"] = "charliethomas"
app.config["PASSWORD"] = "my_password"

# Routes


@app.route("/")
@app.route("/show")
def show():
    """Main Page for blog. It shows all the posts from the db.

    Parameters:
    None

    Template: show.html
    Redirect: None
    """
    context = {
        "posts": get_posts()[::-1]
    }
    return render_template("show.html", **context)


@app.route("/post/<id>")
def post(id):
    """Page for each post. It shows the title and body of a given post.

    Parameters:
    id - init - id for post to view

    Template: post.html
    Redirect: None
    """
    post = get_post(id)
    title = post["title"]
    body = post["body"]
    unicode_body = body.decode("utf-8")
    html_body = markdown.markdown(unicode_body)
    safe_html_body = Markup(html_body)
    context = {
        "title": title,
        "body": safe_html_body
    }
    return render_template("post.html", **context)


@app.route("/update/<id>", methods=["POST", "GET"])
def update(id):
    """Route to update post the function has two operations based on the
    request method.

    Parameters:
    id - init - id for post to update

    GET method:
    If the request method is GET it loads the form to update the post.

    Template: edit.html
    Redirect: None

    POST method:
    If the request method is POST then it updates the post based on the id
    with the title and body.

    Template: None
    Redirect: show
    """
    if request.method == "POST":
        result = update_post(
            id,
            request.form["title"],
            request.form["body"]
        )
        flash(result)
        return redirect(url_for("show"))
    else:
        post = get_post(id)
        return render_template("edit.html", **post)


@app.route("/delete/<id>")
def delete(id):
    """Route to delete post from id.

    Parameters:
    id - int - id for post to delete

    Template: None
    Redirect: show
    """
    result = delete_post(id)
    flash(result)
    return redirect(url_for("show"))


@app.route("/add", methods=["POST", "GET"])
def add():
    """Route to add post. The function has two operations based on the request
    method

    Parameters:
    None

    GET method:
    If the request method is GET it loads the form to add a post.

    Template: add.html
    Redirect: None

    POST method:
    If the request method is POST then it adds the post with the title and
    body.

    Template: None
    Redirect: show
    """
    if request.method == "POST":
        result = add_post(
            request.form["title"],
            request.form["body"]
        )
        flash(result)
        return redirect(url_for("show"))
    else:
        return render_template("add.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    """Route to login. The function has two operations based on the request
    method

    GET method:
    If the request method is GET it loads the form to login.

    Template: login.html
    Redirect: None

    POST method:
    If the request method is POST then it trys tp log the user in. If login
    errors it returns an errors back to login.html. If login is successful
    it redirects to show.

    Template: None
    Redirect: show
    """
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in sucessfully')
            return redirect(url_for('show'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Route to logout.

    Parameters:
    None

    Template: None
    Redirect: show
    """
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show'))


if __name__ == "__main__":
    app.run(debug=True)
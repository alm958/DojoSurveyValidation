from flask import Flask, render_template, request, redirect, flash, session
app = Flask(__name__)
app.secret_key = 'supersecret'
# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template("index.html")

# this route will handle our form submission
# notice how we defined which HTTP methods are allowed by this route
@app.route('/result', methods=['POST'])
def create_result():
    session['name'] = request.form['name']
    session['location'] = request.form['location']
    session['language'] = request.form['language']
    session['comment'] = request.form['comment']
    if len(request.form['name']) < 1 or len(request.form['comment']) < 1:
        if len(request.form['name']) < 1:
            flash("Name cannot be empty!")
        if len(request.form['comment']) < 1:
            flash("Comment cannot be empty!")
        return redirect('/')
    return render_template('show.html')

@app.route('/reset', methods=['POST','get'])
def reset():
    session.pop('name',None)
    session.pop('location',None)
    session.pop('language', None)
    session.pop('comment',None)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

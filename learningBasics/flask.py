from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

# @app.route('/admin')
# def hello_admin():
#    return 'Hello Admin'

# @app.route('/guest/<guest>')
# def hello_guest(guest):
#    return 'Hello %s as Guest' % guest

# @app.route('/user/<name>')
# def hello_user(name):
#    if name =='admin':
#       return redirect(url_for('hello_admin'))
#    else:
#       return redirect(url_for('hello_guest',guest = name))
#-------------------------------------------------------------------------------------

# @app.route('/success/<name>')
# def success(name):
#     return 'Welcome %s in flaskZone!' %name

# @app.route('/login', methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name = user))
#     else:
#         user = request.args.get('nm')
        # return redirect(url_for('success', name = user))
#---------------------------------------------------------------------------------------

# @app.route('/')
# def index():
#     return '<html><body><h1>Hello World</h1></body></html>'
#---------------------------------------------------------------------------------------

# @app.route('/<int:score>')
# def hello(score):
#     # return 'Hello %s' %user
#     return render_template('index.html', marks = score)

@app.route('/result')
def result():
    dict = {'chm' : 'A', 'mth' : 'B', 'phy' : 'C'}
    return render_template('index.html', result = dict)


if __name__ == '__main__':
   app.run(debug = True)

   #x-special/nautilus-clipboard
# c?opy


from wolk import app

@app.route('/')
@app.route('/index')
def index():
    #return render_template('index.html')
    return 'hello world'

@app.route('/aws')
def aws():
    return 'AWS page'

@app.route('/azure')
def azure():
    return 'Microsoft Azure page'

@app.route('/gcp')
def gcp():
    return 'GCP'
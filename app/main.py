from flask import Flask, render_template, request
from database import google_data, insert_main_data, view_all_content, view_all_fields, select_content
app = Flask(__name__)

@app.route('/')
def index():
    content = view_all_content('byte1')
    fields = view_all_fields('byte1')
    update_content = insert_main_data(google_data(), 'byte1')
    return render_template('index.html', content=content, labels=fields, update_content=update_content)

@app.route('/search', methods=["GET", "POST"])
def search():
    fields = view_all_fields('byte1')
    if request.method == "POST":
      data = dict(request.form)
      content = select_content('byte1', data["search"])
    else:
      content = []
    return render_template('search.html', content=content, labels=fields)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)

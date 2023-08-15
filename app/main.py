from flask import Flask, render_template
from database import google_data, insert_main_data, view_all_content, view_all_fields
app = Flask(__name__)

@app.route('/')
def index():
    content = view_all_content('byte2')
    fields = view_all_fields('byte2')
    return render_template('index.html', content=content, labels=fields)

#insert_main_data(google_data(), 'byte1')
#insert_main_data(google_data(), 'byte2')
#view_data_db('byte2')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)

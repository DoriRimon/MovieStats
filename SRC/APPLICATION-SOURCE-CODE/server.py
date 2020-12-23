from flask import Flask, render_template, request
import csv
import os.path



app = Flask(__name__)
PORT = 44444
HOST = 'delta-tomcat-vm'

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "/static/data/filename.csv")
with open(path) as f:
    test = list(csv.reader(f))
    print(test)

# with open('MovieStats\SRC\APPLICATION-SOURCE-CODE\static\data\filename.csv') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for i in range(max(5, len(spamreader))):
#         print(', '.join(spamreader[i]))

# print('here')
# df = pandas.read_csv('/static/data/filename.csv')
# df.head()

@app.route('/search')
def search_return_html():
    query = request.args.get('query')
    # with connector get to your mysql server and query the DB
    # return the answer to number_of_songs var.
    number_of_songs = 5 #should be retrieved from the DB
    return render_template('searchResults.html', count=5, query=query)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':  
    app.run(host=HOST, port=str(PORT), debug=True)
    print('server running at port ', PORT)
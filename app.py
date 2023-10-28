from flask import Flask, request, render_template
import stockpickerbeta

app = Flask(__name__, template_folder='templates')


# Your previous code for data retrieval and sentiment analysis here.

@app.route('/')
def index():
    # This is the main page of your web app where users can input sectors and get recommendations.
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    sector = request.form['sector']  # Get the sector from the user's input.
    recommendations = stockpickerbeta.recommend_stocks(sector)  # Use your recommendation function here.
    return render_template('recommend.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

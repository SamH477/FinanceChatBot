from flask import Flask, request, render_template
import stockpickerbeta

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    ticker = request.form['ticker']  # Get the ticker from the user's input.
    recommendations = stockpickerbeta.recommend_stocks(ticker)  # Use your recommendation function here.
    return render_template('recommend.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)


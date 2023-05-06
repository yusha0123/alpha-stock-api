from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return jsonify("Hello from FLASK!")


@app.route('/top_gainers', methods=['GET'])
@cross_origin()
def top_gainers():
    url = "https://finance.yahoo.com/gainers"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        data.append({
            "symbol": cols[0].text.strip(),
            "name": cols[1].text.strip(),
            "price": cols[2].text.strip(),
            "change": cols[3].text.strip(),
            "percent_change": cols[4].text.strip(),
        })
    return jsonify(data)


@app.route('/top_losers', methods=['GET'])
@cross_origin()
def top_losers():
    url = "https://finance.yahoo.com/losers"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        data.append({
            "symbol": cols[0].text.strip(),
            "name": cols[1].text.strip(),
            "price": cols[2].text.strip(),
            "change": cols[3].text.strip(),
            "percent_change": cols[4].text.strip(),
        })
    return jsonify(data)


@app.route('/stock/<symbol>', methods=['GET'])
@cross_origin()
def get_stock_details(symbol):
    url = f'https://finance.yahoo.com/quote/{symbol}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check for 404 error
    if response.status_code == 404:
        return jsonify({'error': f'Symbol "{symbol}" not found'}), 400

    # Check for NoneType error
    if not soup.find('div', {'id': 'quote-market-notice'}):
        return jsonify({'error': f'Unable to retrieve data for symbol "{symbol}"'}), 400

    # Extract stock details
    stock_details = {}
    stock_details['symbol'] = symbol
    stock_details['name'] = soup.find('h1', {"class":  'D(ib)'}).text
    stock_details['open'] = soup.find(
        'td', {'data-test': 'OPEN-value'}).text
    stock_details['days_range'] = soup.find(
        'td', {'data-test': 'DAYS_RANGE-value'}).text
    stock_details['volume'] = soup.find(
        'td', {'data-test': 'TD_VOLUME-value'}).text
    stock_details['market_cap'] = soup.find(
        'td', {'data-test': 'MARKET_CAP-value'}).text
    stock_details['previous_close'] = soup.find(
        'td', {'data-test': 'PREV_CLOSE-value'}).text
    stock_details['52_week_range'] = soup.find(
        'td', {'data-test': 'FIFTY_TWO_WK_RANGE-value'}).text

    return jsonify(stock_details)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

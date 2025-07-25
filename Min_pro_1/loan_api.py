from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/loan/calculate', methods=['POST'])
def calculate_emi():
    data = request.get_json()
    try:
        amount = float(data.get('amount'))
        interest = float(data.get('interest'))
        years = int(data.get('years'))

        if amount <= 0 or interest <= 0 or years <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({'error': 'All fields must be numeric and > 0'}), 400

    r = interest / (12 * 100)  # Monthly interest rate
    n = years * 12             # Total months

    emi = (amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    emi = round(emi, 2)

    return jsonify({
        'amount': amount,
        'interest': interest,
        'years': years,
        'monthly_emi': emi
    })
    
if __name__ == '__main__':
    app.run(debug=True)

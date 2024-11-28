from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load data from CSV files
grade_data = {
    'Grade 3': pd.read_csv('grade3.csv'),
    # 'Grade 4': pd.read_csv('grade4.csv'),
    # 'Grade 5': pd.read_csv('grade5.csv'),
    # 'Grade 6': pd.read_csv('grade6.csv'),
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    week = request.args.get('week')
    grade = request.args.get('grade')

    if not week and not grade:
        return jsonify({"error": "Please provide either a week or a grade to search."}), 400

    results = []
    if week:
        try:
            week = int(week)
            for grade_name, data in grade_data.items():
                week_data = data[data['Week Number'] == week].to_dict('records')
                results.extend([{**row, 'Grade': grade_name} for row in week_data])
        except ValueError:
            return "Error: Week must be a valid number.", 400
    elif grade:
        try:
            grade = int(grade)
            data = grade_data.get(f'Grade {grade}')
            if data is not None:
                results = [{**row, 'Grade': f'Grade {grade}'} for row in data.to_dict('records')]
            else:
                return f"Error: No data found for Grade {grade}.", 404
        except ValueError:
            return f"Error: Grade must be a valid number.", 400

    if not results:
        return "No matching records found.", 404

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

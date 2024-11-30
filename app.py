from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load data from CSV files
grade_data = {
    'Grade 3': pd.read_csv('/Users/zoulaimi/Documents/GitHub/Weekly-Lesson-Finder/grade3.csv'),
    'Grade 4': pd.read_csv('/Users/zoulaimi/Documents/GitHub/Weekly-Lesson-Finder/grade4.csv'),
    'Grade 5': pd.read_csv('/Users/zoulaimi/Documents/GitHub/Weekly-Lesson-Finder/grade5.csv'),
    'Grade 6': pd.read_csv('/Users/zoulaimi/Documents/GitHub/Weekly-Lesson-Finder/grade6.csv'),
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    week = request.args.get('week')
    grade = request.args.get('grade')
    topic = request.args.get('topic')
    code = request.args.get('code')


    if not (week or grade or topic or code):
        return "Error: Please provide either a week, a grade, a topic or a code to search.", 400

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
            return "Error: Grade must be a valid number.", 400
    
    elif topic:
        for grade_name, data in grade_data.items():
            topic_data = data[data['Topic'].str.contains(topic, case=False, na=False)].to_dict('records')
            results.extend([{**row, 'Grade': grade_name} for row in topic_data])

    elif code:
        for grade_name, data in grade_data.items():
            code_data = data[data['Code'].fillna('').str.contains(code, case=False)].to_dict('records')
            results.extend([{**row, 'Grade': grade_name} for row in code_data])

    if not results:
        return "No matching records found.", 404

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

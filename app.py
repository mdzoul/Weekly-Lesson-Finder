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

@app.route('/readme')
def readme():
    return render_template('README.html')

@app.route('/search', methods=['GET'])
def search():
    # week = request.args.get('week')
    # grade = request.args.get('grade')
    # topic = request.args.get('topic')
    # code = request.args.get('code')


    # if not (week or grade or topic or code):
    #     return "Error: Please provide either a week, a grade, a topic or a code to search.", 400

    # results = []

    # if week:
    #     try:
    #         week = int(week)
    #         for grade_name, data in grade_data.items():
    #             week_data = data[data['Week Number'] == week].to_dict('records')
    #             results.extend([{**row, 'Grade': grade_name} for row in week_data])
    #     except ValueError:
    #         return "Error: Week must be a valid number.", 400
    
    # elif grade:
    #     try:
    #         grade = int(grade)
    #         data = grade_data.get(f'Grade {grade}')
    #         if data is not None:
    #             results = [{**row, 'Grade': f'Grade {grade}'} for row in data.to_dict('records')]
    #         else:
    #             return f"Error: No data found for Grade {grade}.", 404
    #     except ValueError:
    #         return "Error: Grade must be a valid number.", 400
    
    # elif topic:
    #     for grade_name, data in grade_data.items():
    #         topic_data = data[data['Topic'].str.contains(topic, case=False, na=False)].to_dict('records')
    #         results.extend([{**row, 'Grade': grade_name} for row in topic_data])

    # elif code:
    #     for grade_name, data in grade_data.items():
    #         code_data = data[data['Code'].fillna('').str.contains(code, case=False)].to_dict('records')
    #         results.extend([{**row, 'Grade': grade_name} for row in code_data])

    # if not results:
    #     return "No matching records found.", 404

    # return render_template('results.html', results=results)

    # Determine the type of input

    query = request.args.get('query', '').strip()  # Get the input from the single search bar

    if not query:
        return "Error: Please provide a search input.", 400

    results = []

    if query.isdigit():
        # If it's numeric, treat it as a week number
        week = int(query)
        for grade_name, data in grade_data.items():
            week_data = data[data['Week Number'] == week].to_dict('records')
            results.extend([{**row, 'Grade': grade_name} for row in week_data])

    elif query.lower().startswith('grade'):
        # If it starts with "Grade", treat it as a grade
        grade = query.title()  # Format to "Grade X"
        data = grade_data.get(grade)
        if data is not None:
            results = [{**row, 'Grade': grade} for row in data.to_dict('records')]
        else:
            return f"Error: No data found for {grade}.", 404
        
    elif any('Code' in df.columns and query in df['Code'].fillna('').values for df in grade_data.values()):
        # If it matches a code, search for it in the 'Code' column
        for grade_name, data in grade_data.items():
            code_data = data[data['Code'].fillna('').str.contains(query, case=False)].to_dict('records')
            results.extend([{**row, 'Grade': grade_name} for row in code_data])

    else:
        # Otherwise, treat it as a topic
        for grade_name, data in grade_data.items():
            if 'Topic' in data.columns:
                topic_data = data[data['Topic'].str.contains(query, case=False, na=False)].to_dict('records')
                results.extend([{**row, 'Grade': grade_name} for row in topic_data])

    if not results:
        return "Error: No matching records found.", 404

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)

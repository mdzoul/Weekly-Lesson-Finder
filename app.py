from flask import Flask, request, jsonify, render_template
import pandas as pd
import re

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

# @app.route('/search', methods=['GET'])
# def search():

#     query = request.args.get('query', '').strip()  # Get the input from the single search bar

#     if not query:
#         return "Error: Please provide a search input.", 400

#     results = []

#     if query.isdigit():
#         # If it's numeric, treat it as a week number
#         week = int(query)
#         for grade_name, data in grade_data.items():
#             week_data = data[data['Week Number'] == week].to_dict('records')
#             results.extend([{**row, 'Grade': grade_name} for row in week_data])

#     elif query.lower().startswith('grade'):
#         # If it starts with "Grade", treat it as a grade
#         grade = query.title()  # Format to "Grade X"
#         data = grade_data.get(grade)
#         if data is not None:
#             results = [{**row, 'Grade': grade} for row in data.to_dict('records')]
#         else:
#             return f"Error: No data found for {grade}.", 404
        
#     elif any('Code' in df.columns and query in df['Code'].fillna('').values for df in grade_data.values()):
#         # If it matches a code, search for it in the 'Code' column
#         for grade_name, data in grade_data.items():
#             code_data = data[data['Code'].fillna('').str.contains(query, case=False)].to_dict('records')
#             results.extend([{**row, 'Grade': grade_name} for row in code_data])

#     else:
#         # Otherwise, treat it as a topic
#         for grade_name, data in grade_data.items():
#             if 'Topic' in data.columns:
#                 topic_data = data[data['Topic'].str.contains(query, case=False, na=False)].to_dict('records')
#                 results.extend([{**row, 'Grade': grade_name} for row in topic_data])

#     if not results:
#         return "Error: No matching records found.", 404

#     return render_template('results.html', results=results)

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('query', '')

    if not query:
        return jsonify({"error": "Please provide a search input."}), 400

    results = []

    # Helper function to convert dashes to an unordered list
    def format_as_list(text):
        if isinstance(text, str) and '-' in text:
            items = [item.strip() for item in text.split('- ') if item.strip()]
            return '<ul>' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>'
        return text
    
    # Helper function to clean NaN values
    def clean_row(row):
        return {key: ('' if pd.isna(value) else value) for key, value in row.items()}
    
    query = query.upper() if query.lower().startswith('ass') else query  # Normalize the query for code searches

    # Determine if query matches a topic code pattern (e.g., X.X or X.X.X)
    topic_code_pattern = re.compile(r'^\d+\.\d+(\.\d+)?$')  # Matches X.X or X.X.X format
    is_topic_code = bool(topic_code_pattern.match(query.upper()))

    # Determine the type of input
    if query.isdigit():
        week = int(query)
        for grade_name, data in grade_data.items():
            week_data = data[data['Week Number'] == week].dropna(how='all').to_dict('records')
            for row in week_data:
                row = clean_row(row)  # Clean NaN values
                row['Content'] = format_as_list(row.get('Content', ''))
                row['Activities'] = format_as_list(row.get('Activities', ''))
                results.append({**row, 'Grade': grade_name})

    elif query.lower().startswith('grade'):
        grade = query.title()  # Normalize query to match "Grade X"
        if grade in grade_data:
            data = grade_data[grade].dropna(how='all')  # Drop completely empty rows
            for row in data.to_dict('records'):
                row = clean_row(row)  # Clean NaN values
                row['Content'] = format_as_list(row.get('Content', ''))
                row['Activities'] = format_as_list(row.get('Activities', ''))
                results.append({**row, 'Grade': grade})
        else:
            return jsonify({"error": f"No data found for {grade}."}), 404
        
    elif is_topic_code:
        for grade_name, data in grade_data.items():
            if 'Code' in data.columns:
                code_data = data[data['Code'].fillna('').str.contains(query, case=False, na=False)].to_dict('records')
                for row in code_data:
                    row = clean_row(row)
                    row['Content'] = format_as_list(row.get('Content', ''))
                    row['Activities'] = format_as_list(row.get('Activities', ''))
                    results.append({**row, 'Grade': grade_name})
        
    elif query.upper().startswith('ASS'):
        for grade_name, data in grade_data.items():
            if 'Code' in data.columns:
                code_data = data[data['Code'].fillna('').str.startswith(query.upper())].to_dict('records')
                for row in code_data:
                    row = clean_row(row)
                    row['Content'] = format_as_list(row.get('Content', ''))
                    row['Activities'] = format_as_list(row.get('Activities', ''))
                    results.append({**row, 'Grade': grade_name})
                    
    else:
        for grade_name, data in grade_data.items():
            if 'Topic' in data.columns:
                topic_data = data[data['Topic'].str.contains(query, case=False, na=False)].to_dict('records')
                for row in topic_data:
                    row = clean_row(row)  # Clean NaN values
                    row['Content'] = format_as_list(row.get('Content', ''))
                    row['Activities'] = format_as_list(row.get('Activities', ''))
                    results.append({**row, 'Grade': grade_name})

    if not results:
        return jsonify({"error": "No matching records found."}), 404

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

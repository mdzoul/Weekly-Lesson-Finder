# Weekly Lesson Finder

**Weekly Lesson Finder** is a web application designed to help educators and curriculum specialists quickly find and access weekly lesson plans. The tool is ideal for simplifying lesson planning and improving organization.

## Features

- Search lesson plans by **week number**, **grade** (Grades 3 to 6), **topic**, or **code**.
- View detailed lesson information including:
  - Objectives
  - Topics
  - Activities
  - Type of activity
  - Lesson title
  - Week number
- User-friendly interface with intuitive navigation.
- Built using **Flask** for the backend and **HTML/CSS** for the frontend.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mdzoul/weekly-lesson-finder.git
   cd weekly-lesson-finder
   ```

2. Install dependencies:

   ```bash
   pip install flask pandas
   ```

3. Run the Flask app:

   ```
   python app.py
   ```

4. Open your browser and navigate to:

   ```
   http://127.0.0.1:5000
   ```

## Usage

1. **Search Options**: Use the search bar to enter a week number, grade (e.g., "Grade 3"), topic, or code to find relevant lesson plans.

2. **View Results**: Results will display the grade, week number, topic, code, lesson title, objectives, content, type of activity, and activities.

3. **Navigation**: Use the "Back to Search" button to return to the search page after viewing results.

## File Structure

- `/static/css/styles.css`: Contains the CSS styles for the application.
- `/templates/`: Contains all HTML templates used by the application, such as the main search page and results page.
- `/app.py`: The main application file that handles routing and data processing.
- `/gradeX.csv`: CSV files containing lesson data for each grade (Grade 3 to Grade 6).

## About the Creator

This project is developed by a science teacher who loves to code and aims to simplify lesson planning for educators. The Weekly Lesson Finder is a personal project designed to make lesson planning more efficient and organized.

## Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to create a pull request or open an issue.

# search.py
"""
This module provides a Search class for performing content searches on grade-level data stored in CSV files.
The search supports queries by week number, grade level, topic code, or topic name.
It handles data loading, formatting, and cleaning of NaN values.
The `format_as_list` method formats a string containing dash-separated items into an HTML unordered list.
The `clean_row` method cleans a dictionary representing a row, replacing NaN values with empty strings.
The `search` method performs the actual search on the loaded data, and returns a list of matching records (dictionaries)
with an additional "Grade" key, or an error message and corresponding HTTP status code.
"""

import re
from pathlib import Path

import pandas as pd


class Search:
    """
    A class to perform content searches on grade-level data.

    Attributes:
        grade_data (dict): A dictionary containing pandas DataFrames for each grade level.
        script_dir (Path): The directory of the current script.
    """

    def __init__(self, data_dir="data"):
        """Initializes the Search object by loading the grade data from CSV files."""
        self.script_dir = Path(__file__).parent
        self.grade_data = {
            "Grade 3": pd.read_csv(self.script_dir / data_dir / "grade3.csv"),
            "Grade 4": pd.read_csv(self.script_dir / data_dir / "grade4.csv"),
            "Grade 5": pd.read_csv(self.script_dir / data_dir / "grade5.csv"),
            "Grade 6": pd.read_csv(self.script_dir / data_dir / "grade6.csv"),
        }

    def format_as_list(self, text):
        """Formats a string containing dash-separated items into an HTML unordered list."""
        if isinstance(text, str) and "-" in text:
            items = [item.strip() for item in text.split("- ") if item.strip()]
            return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"
        return text

    def clean_row(self, row):
        """Cleans a dictionary representing a row, replacing NaN values with empty strings."""
        return {key: ("" if pd.isna(value) else value) for key, value in row.items()}

    def search(self, query):
        """Performs a search on the loaded grade data based on the provided query."""
        if not query:
            return {"error": "Please provide a search input."}, 400

        results = []

        query = (
            query.upper() if query.lower().startswith("ass") else query
        )  # Normalize the query for code searches

        # Determine if query matches a topic code pattern (e.g., X.X or X.X.X)
        topic_code_pattern = re.compile(
            r"^\d+\.\d+(\.\d+)?$"
        )  # Matches X.X or X.X.X format
        is_topic_code = bool(topic_code_pattern.match(query.upper()))

        if query.isdigit():
            week = int(query)
            for grade_name, data in self.grade_data.items():
                week_data = (
                    data[data["Week Number"] == week]
                    .dropna(how="all")
                    .to_dict("records")
                )
                for row in week_data:
                    row = self.clean_row(row)  # Clean NaN values
                    row["Content"] = self.format_as_list(row.get("Content", ""))
                    row["Activities"] = self.format_as_list(row.get("Activities", ""))
                    results.append({**row, "Grade": grade_name})

        elif query.lower().startswith("grade"):
            grade = query.title()  # Normalize query to match "Grade X"
            if grade in self.grade_data:
                data = self.grade_data[grade].dropna(
                    how="all"
                )  # Drop completely empty rows
                for row in data.to_dict("records"):
                    row = self.clean_row(row)  # Clean NaN values
                    row["Content"] = self.format_as_list(row.get("Content", ""))
                    row["Activities"] = self.format_as_list(row.get("Activities", ""))
                    results.append({**row, "Grade": grade})
            else:
                return {"error": f"No data found for {grade}."}, 404

        elif is_topic_code:
            for grade_name, data in self.grade_data.items():
                if "Code" in data.columns:
                    code_data = data[
                        data["Code"]
                        .fillna("")
                        .str.contains(query, case=False, na=False)
                    ].to_dict("records")
                    for row in code_data:
                        row = self.clean_row(row)
                        row["Content"] = self.format_as_list(row.get("Content", ""))
                        row["Activities"] = self.format_as_list(
                            row.get("Activities", "")
                        )
                        results.append({**row, "Grade": grade_name})

        elif query.upper().startswith("ASS"):
            for grade_name, data in self.grade_data.items():
                if "Code" in data.columns:
                    code_data = data[
                        data["Code"].fillna("").str.startswith(query.upper())
                    ].to_dict("records")
                    for row in code_data:
                        row = self.clean_row(row)
                        row["Content"] = self.format_as_list(row.get("Content", ""))
                        row["Activities"] = self.format_as_list(
                            row.get("Activities", "")
                        )
                        results.append({**row, "Grade": grade_name})

        else:
            for grade_name, data in self.grade_data.items():
                if "Topic" in data.columns:
                    topic_data = data[
                        data["Topic"].str.contains(query, case=False, na=False)
                    ].to_dict("records")
                    for row in topic_data:
                        row = self.clean_row(row)  # Clean NaN values
                        row["Content"] = self.format_as_list(row.get("Content", ""))
                        row["Activities"] = self.format_as_list(
                            row.get("Activities", "")
                        )
                        results.append({**row, "Grade": grade_name})

        if not results:
            return {"error": "No matching records found."}, 404

        return results, 200

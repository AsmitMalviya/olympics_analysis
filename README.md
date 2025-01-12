# olympics_analysis
"An interactive Streamlit app for Olympics data analysis."

# 🏅 Olympics Analysis Dashboard

Welcome to the **Olympics Analysis Dashboard**, an interactive web application built using [Streamlit](https://streamlit.io). This project provides insights into 120 years of Olympic history, offering analysis of trends, medal tallies, athlete statistics, and more.

---

## 📊 Features

### 🎯 Medal Tally
- View the medal tally for any country and year.
- Analyze trends in medal performance over time.

### 📈 Overall Analysis
- Examine the evolution of the Olympics, including:
  - Participating nations.
  - Number of athletes, sports, and events.
  - Gender representation trends over the years.

### 🌍 Country-Wise Analysis
- Focus on a specific country’s performance in the Olympics.
- Explore which sports the country excels in.
- View the top athletes from any country.

### 🏋️ Athlete-Wise Analysis
- Analyze individual athlete performances.
- Visualize age distribution by medal type.
- Explore height and weight trends across different sports.

---

## 📂 Project Structure
/olympics_analysis/ │ ├── app.py # Main Streamlit app for the dashboard ├── helper.py # Helper functions for analysis ├── preprocessor.py # Data preprocessing logic ├── athlete_events.csv # Dataset with athlete performance details ├── noc_regions.csv # Dataset mapping NOC codes to regions ├── requirements.txt # Required Python libraries ├── README.md # Project documentation ├── .gitignore # Files and folders to ignore in Git │ ├── datasets/ # Directory for datasets │ ├── athlete_events.csv # Main dataset │ └── noc_regions.csv # Supplementary dataset │ ├── static/ # Directory for static files (images, CSS, etc.) │ └── lottie_animation.json # Lottie animation for the app │ └── templates/ # Directory for HTML templates (if applicable) ├── index.html # Main HTML template └── analysis.html # Template for analysis results


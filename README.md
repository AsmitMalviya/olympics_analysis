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

- **/olympics_analysis/**  
  - **app.py**: Main Streamlit app for the dashboard.  
  - **helper.py**: Helper functions for analysis.  
  - **preprocessor.py**: Preprocessing logic for cleaning and transforming data.  
  - **athlete_events.csv**: Dataset with athlete performance details.  
  - **noc_regions.csv**: Dataset mapping NOC codes to regions.  
  - **requirements.txt**: List of Python libraries required to run the project.  
  - **README.md**: Project documentation.  
  - **.gitignore**: Specifies files and folders to ignore in Git.  

- **datasets/**: Directory for datasets.  
  - **athlete_events.csv**: Main dataset.  
  - **noc_regions.csv**: Supplementary dataset.  

- **static/**: Directory for static files (images, CSS, etc.).  
  - **lottie_animation.json**: Lottie animation for the app.  

- **templates/**: Directory for HTML templates (if applicable).  
  - **index.html**: Main HTML template.  
  - **analysis.html**: Template for analysis results.  

## 🗂️ Dataset

The analysis is based on the dataset **"120 Years of Olympic History: Athletes and Results"**, available on Kaggle.

- **Dataset Link**: [120 Years of Olympic History - Kaggle](https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results)

### Dataset Description:
1. **Athlete Events Dataset** (`athlete_events.csv`):  
   - Contains detailed information about Olympic athletes from 1896 to 2016:
     - Name, age, sex, and nationality.
     - Sport and event.
     - Medals won.
2. **NOC Regions Dataset** (`noc_regions.csv`):  
   - Maps National Olympic Committees (NOCs) to their respective regions.
  
## 🛠️ Installation and Usage

Follow the steps below to set up and run the Olympics Analysis Dashboard on your local machine:

### 1. Clone the Repository
Clone this repository to your local machine using the following command:
```bash
git clone https://github.com/AsmitMalviya/olympics_analysis.git
cd olympics_analysis
```

### 2. Install Dependencies
Ensure you have Python 3.7+ installed. Then, install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit App
Start the Streamlit server by running:
```bash
streamlit run app.py
```
This will launch the app in your default web browser. If it doesn’t open automatically, navigate to http://localhost:8501.


## 🚀 Live Demo
Check out the live version of the app here: [Olympics Analysis Dashboard](https://olympics-insights.streamlit.app/)

## 🎥 Screenshots
  
### 1. Welcome Screen  
![Welcome Screen](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20191639.png?raw=true)

### 2. Medal Tally Section
![Medal Tally Section](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20191910.png?raw=true)

### 3. Country-Wise Analysis
![Country-Wise Analysis](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20192520.png?raw=true)
![Country-Wise Analysis](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20192611.png?raw=true)

### 4. Overall Analysis
![Overall Analysis](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20192653.png?raw=true)
![Overall Analysis](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20192916.png?raw=true)

### 5. Athlete-Wise Analysis
![Athlete-Wise Analysis](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20193109.png?raw=true)
![Athlete-Wise Analysis](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20193128.png?raw=true)
![Athlete-Wise Analysis](https://github.com/AsmitMalviya/olympics_analysis/blob/main/screenshot/Screenshot%202025-01-14%20193151.png?raw=true)

## Technologies Used
- **app.py**: Main Streamlit app for the dashboard.  

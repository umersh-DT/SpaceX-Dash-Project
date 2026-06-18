# SpaceX-Dash-Project
# SpaceX Falcon 9 First-Stage Landing Prediction

## Project Overview
This repository contains the complete data science pipeline built to predict the landing success of SpaceX Falcon 9 first-stage boosters. By utilizing telemetry data, spatial visual analytics, and machine learning classification algorithms, this project determines if a booster can be successfully recovered—directly impacting competitive launch pricing evaluation ($62M reusable vs. $165M expendable frameworks).

## Repository Structure
* `/notebooks`: Contains data collection, wrangling, SQL EDA, and visualization notebooks.
* `/dashboards`: Contains the interactive operational dashboard (`spacex_dash_app.py`).
* `requirements.txt`: Python package configuration environments.

## Core Methodologies Applied
1. **Data Ingestion:** REST API normalization & BeautifulSoup HTML web scraping.
2. **Exploratory Data Analysis:** SQLite structured querying & Seaborn statistical charting.
3. **Interactive Analytics:** Folium proximity maps & Plotly Dash multi-callback dashboards.
4. **Predictive Modeling:** Hyperparameter tuning via 10-Fold GridSearchCV across Logistic Regression, SVM, Decision Trees, and KNN architectures.

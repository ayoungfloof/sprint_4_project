# Car Sales Dashboard

## Project Overview

This project is a web-based data dashboard built using Streamlit, aimed at visualizing U.S. car sales data. Users can interact with various aspects of the data such as price distributions, days listed, vehicle conditions, and more. The dashboard provides customizable visualizations to explore trends in car sales based on the selected filters.

### Key Features:
- **Histograms** that show the distribution of prices and days listed by manufacturer.
- **Bar charts** visualizing average prices based on odometer readings and vehicle types.
- **Scatter plots** for exploring price versus odometer readings, categorized by vehicle condition.
- **Custom filters** to analyze data by manufacturer, vehicle type, and model year.

### Visualizations Included:
1. **Dataset cleaning and preparation**
2. **Histogram**: Distribution of Days Listed by Manufacturer
3. **Histogram**: Price Distribution by Manufacturer
4. **Bar Plot**: Average Price by Odometer Range and Vehicle Type
5. **Scatter Plot**: Price vs. Odometer by Vehicle Condition
6. **Bar Plot**: Average Price by Odometer Range for Manufacturers and Vehicle Types
7. **Bar Plot**: Average Price vs. Model Year for Selected Manufacturer and Vehicle Type
8. **Bar Plot**: Average Price by Vehicle Type and Transmission

## How to Access the Web Application

The Car Sales Dashboard is deployed and can be accessed via the following link:

[**Car Sales Dashboard Web App**](https://your-app-link-here)  

Simply click on the link to launch the dashboard in your web browser and start exploring the visualizations.

## Technologies and Libraries Used

- **[Streamlit](https://streamlit.io/)**: For creating the interactive web application.
- **[Pandas](https://pandas.pydata.org/)**: For data manipulation and cleaning.
- **[Plotly](https://plotly.com/python/)**: To create dynamic and interactive data visualizations.
  
### Data Processing Methods:
- **Data Cleaning**: Missing data fields were handled, outliers were removed, and appropriate data types were assigned to ensure consistency.
- **Data Visualization**: Custom plots and charts were created to allow users to visually explore trends in car sales data.

## Dataset Information

The dataset used in this project is related to used car sales in the U.S. and includes the following features:
- **Manufacturer**: Brand of the car.
- **Model Year**: Year the car was manufactured.
- **Price**: Sale price of the vehicle.
- **Odometer**: Number of miles driven by the vehicle.
- **Vehicle Condition**: Condition of the vehicle (e.g., new, like new, etc.).
- **Transmission**: Transmission type (automatic or manual).

## Project Structure

- **app.py**: This file contains the Streamlit code that builds and runs the dashboard.
- **vehicles_us.csv**: The dataset used for analysis and visualizations.
- **README.md**: This file, which contains project documentation.

## Live Application
To view and interact with the dashboard live, use this URL:

https://carsalesdashboard.onrender.com

## Running Locally

To run this project locally on your machine, follow the steps below:

1. Clone this repository:
   ```bash
   git clone https://github.com/ayoungfloof/sprint_4_project.git
import streamlit as st
import pandas as pd
import plotly.express as px

# Set a title
st.title('Car Sales Dashboard')

# Display a text message
st.write('Welcome to the Car Sales Dashboard!')

# Load the dataset
df = pd.read_csv('vehicles_us.csv')

# Data cleaning process (hidden)
df['model_year'].fillna('unknown', inplace=True)
df['odometer'].fillna(df['odometer'].median(), inplace=True)
df['cylinders'].fillna(df['cylinders'].mode()[0], inplace=True)
df['paint_color'].fillna('unknown', inplace=True)
df['is_4wd'].fillna(0, inplace=True)
df = df[(df['price'] > 500) & (df['price'] < 100000)]
df = df[df['odometer'] < 500000]
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['model_year'] = pd.to_numeric(df['model_year'], errors='coerce')
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce')
df['cylinders'] = pd.to_numeric(df['cylinders'], errors='coerce')
df = df.drop_duplicates()

# Create 'manufacturer' column by extracting the first word from 'model'
df['manufacturer'] = df['model'].str.split().str[0]

# Insert code to create the 'odometer_range' column here:
# Bin the odometer readings into ranges for the bar plot
bins = [0, 25000, 50000, 75000, 100000, 150000, 200000, 250000, 300000]
labels = ['0-25K', '25K-50K', '50K-75K', '75K-100K', '100K-150K', '150K-200K', '200K-250K', '250K+']
df['odometer_range'] = pd.cut(df['odometer'], bins=bins, labels=labels)

# Display cleaned data with scrollbars
st.subheader('Cleaned Dataset Overview')
st.dataframe(df)

# Streamlit section for filtering manufacturers and displaying the first histogram
st.subheader('Distribution of Days Listed by Manufacturer')

# Let the user select up to three manufacturers
manufacturers = df['manufacturer'].unique()
manufacturer_1 = st.selectbox('Select Manufacturer 1', manufacturers)
manufacturer_2 = st.selectbox('Select Manufacturer 2', manufacturers)
manufacturer_3 = st.selectbox('Select Manufacturer 3', manufacturers)

# Filter data based on selected manufacturers
selected_manufacturers = [manufacturer_1, manufacturer_2, manufacturer_3]
filtered_df = df[df['manufacturer'].isin(selected_manufacturers)]

# Create and display the first histogram
fig = px.histogram(
    filtered_df,
    x='days_listed',
    color='manufacturer',
    title='Distribution of Days Listed by Selected Manufacturers',
    labels={'days_listed': 'Days Listed', 'count': 'Number of Vehicles'},
    barmode='overlay',
    nbins=20
)

# Update the layout of the plot
fig.update_layout(
    yaxis=dict(title='Number of Vehicles', showgrid=True, gridcolor='lightgray', gridwidth=1),
    xaxis=dict(title='Days Listed', showgrid=False)
)

# Display the first histogram
st.plotly_chart(fig)

# Streamlit section for filtering manufacturers and displaying the second histogram
st.subheader('Price Distribution by Manufacturer')

# Let the user select up to three manufacturers
manufacturer_1_price = st.selectbox('Select Manufacturer 1 for Price', manufacturers)
manufacturer_2_price = st.selectbox('Select Manufacturer 2 for Price', manufacturers)
manufacturer_3_price = st.selectbox('Select Manufacturer 3 for Price', manufacturers)

# Filter data for the second histogram
selected_manufacturers_price = [manufacturer_1_price, manufacturer_2_price, manufacturer_3_price]
filtered_df_price = df[df['manufacturer'].isin(selected_manufacturers_price)]

# Create and display the second histogram
fig2 = px.histogram(
    filtered_df_price,
    x='price',
    color='manufacturer',
    title='Price Distribution for Selected Manufacturers',
    labels={'price': 'Price (USD)', 'count': 'Number of Vehicles'},
    barmode='overlay',
    nbins=30
)

# Update the layout of the second plot
fig2.update_layout(
    yaxis=dict(title='Number of Vehicles', showgrid=True, gridcolor='lightgray', gridwidth=1),
    xaxis=dict(title='Price (USD)', showgrid=False)
)

# Display the second histogram
st.plotly_chart(fig2)

# Streamlit section for selecting vehicle types and displaying the odometer-based histogram
st.subheader('Average Price by Odometer Range and Vehicle Type')

# Let the user select three vehicle types
vehicle_types = df['type'].unique()
vehicle_type_1 = st.selectbox('Select Vehicle Type 1', vehicle_types, index=0)
vehicle_type_2 = st.selectbox('Select Vehicle Type 2', vehicle_types, index=1)
vehicle_type_3 = st.selectbox('Select Vehicle Type 3', vehicle_types, index=2)

# Filter data based on selected vehicle types
selected_types = [vehicle_type_1, vehicle_type_2, vehicle_type_3]
filtered_df_odometer = df[df['type'].isin(selected_types)][['type', 'odometer_range', 'price']]

# Group by 'type' and 'odometer_range' and calculate the average price
avg_price_by_type_odometer = filtered_df_odometer.groupby(['type', 'odometer_range'])['price'].mean().reset_index()

# Create and display the odometer-range-based histogram
fig3 = px.bar(
    avg_price_by_type_odometer,
    x='odometer_range',
    y='price',  # Compare by price
    color='type',  # Color by vehicle type
    barmode='group',  # Group bars side by side
    title=f'Average Price by Odometer Range for Selected Vehicle Types',
    labels={'price': 'Average Price (USD)', 'odometer_range': 'Odometer Range (Miles)'}
)

# Update layout to add grid lines
fig3.update_layout(
    yaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1),
    xaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1)
)

# Display the odometer-range-based histogram
st.plotly_chart(fig3)

# Streamlit section for displaying scatter plot of Price vs. Odometer
st.subheader('Scatter Plot: Price vs. Odometer by Vehicle Condition')

# Let the user select a vehicle condition
vehicle_conditions = df['condition'].unique()
selected_condition = st.selectbox('Select Vehicle Condition', vehicle_conditions)

# Filter data based on selected vehicle condition
if selected_condition:
    filtered_scatter_df = df[df['condition'] == selected_condition]
else:
    filtered_scatter_df = df

# Create and display scatter plot
fig4 = px.scatter(
    filtered_scatter_df,
    x='odometer',
    y='price',
    color='condition',  # Color by vehicle condition
    title=f'Price vs. Odometer Reading for {selected_condition or "All Conditions"}',
    labels={'price': 'Price (USD)', 'odometer': 'Odometer Reading (Thousands of Miles)'},
    hover_data=['manufacturer', 'model']
)

# Update layout for scatter plot
fig4.update_layout(
    xaxis=dict(
        title='Odometer (Thousands of Miles)',
        showgrid=True,
        gridcolor='lightgray',
        tickvals=[0, 50000, 100000, 150000, 200000, 250000, 300000],  # Define tick values
        ticktext=['0k', '50k', '100k', '150k', '200k', '250k', '300k']  # Custom text with 'k'
    ),
    yaxis=dict(title='Price (USD)', showgrid=True, gridcolor='lightgray'),
    plot_bgcolor='white'
)

# Display scatter plot
st.plotly_chart(fig4)

# Section: Average Price by Odometer Range for Manufacturers and Vehicle Types
st.subheader('Average Price by Odometer Range for Manufacturers and Vehicle Types')

# Let the user select manufacturers and vehicle types for comparison
manufacturer_1 = st.selectbox('Select Manufacturer 1 for Odometer Range Comparison', manufacturers, index=0)
vehicle_type_1 = st.selectbox('Select Vehicle Type 1 for Manufacturer 1', vehicle_types, index=0)
manufacturer_2 = st.selectbox('Select Manufacturer 2 for Odometer Range Comparison', manufacturers, index=1)
vehicle_type_2 = st.selectbox('Select Vehicle Type 2 for Manufacturer 2', vehicle_types, index=1)
manufacturer_3 = st.selectbox('Select Manufacturer 3 for Odometer Range Comparison', manufacturers, index=2)
vehicle_type_3 = st.selectbox('Select Vehicle Type 3 for Manufacturer 3', vehicle_types, index=2)

# Filter data based on selected manufacturers and vehicle types
selected_df = df[
    ((df['manufacturer'] == manufacturer_1) & (df['type'] == vehicle_type_1)) |
    ((df['manufacturer'] == manufacturer_2) & (df['type'] == vehicle_type_2)) |
    ((df['manufacturer'] == manufacturer_3) & (df['type'] == vehicle_type_3))
][['manufacturer', 'type', 'odometer_range', 'price']]

# Group by 'manufacturer', 'type', and 'odometer_range' and calculate the average price
avg_price_by_manufacturer_type_odometer = selected_df.groupby(['manufacturer', 'type', 'odometer_range'])['price'].mean().reset_index()

# Create a new column to reflect only the selected manufacturers and types in the legend
avg_price_by_manufacturer_type_odometer['manufacturer_type'] = avg_price_by_manufacturer_type_odometer['manufacturer'] + " (" + avg_price_by_manufacturer_type_odometer['type'] + ")"

# Restrict the legend to show only selected manufacturers and types
unique_legend_entries = avg_price_by_manufacturer_type_odometer['manufacturer_type'].unique()

# Create and display the bar plot for odometer range comparison
fig5 = px.bar(
    avg_price_by_manufacturer_type_odometer,
    x='odometer_range',
    y='price',
    color='manufacturer_type',
    barmode='group',
    title='Average Price by Odometer Range for Selected Manufacturers and Vehicle Types',
    labels={'price': 'Average Price (USD)', 'odometer_range': 'Odometer Range (Miles)'}
)

# Update layout to add grid lines and improve readability
fig5.update_layout(
    yaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1),
    xaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1),
    legend_title_text='Manufacturer and Vehicle Type'
)

# Ensure only selected manufacturer types appear in the legend
fig5.for_each_trace(
    lambda t: t.update(name=t.name if t.name in unique_legend_entries else None, visible="legendonly" if t.name not in unique_legend_entries else True)
)

# Display the bar plot
st.plotly_chart(fig5)

# Section: Average Price vs. Model Year for Selected Manufacturer and Vehicle Type
st.subheader('Average Price vs. Model Year for Selected Manufacturer and Vehicle Type')

# Let the user select a manufacturer and vehicle type for model year comparison
dropdown_manufacturer = st.selectbox('Select Manufacturer for Model Year Comparison', manufacturers)
dropdown_type = st.selectbox('Select Vehicle Type for Model Year Comparison', vehicle_types)

# Model year slider to limit range
model_year_range = st.slider('Select Model Year Range', min_value=1929, max_value=int(df['model_year'].max()), value=(2000, 2024))

# Filter the data and calculate average price by model year
filtered_df_model_year = df.loc[
    (df['type'] == dropdown_type) & 
    (df['manufacturer'] == dropdown_manufacturer) & 
    (df['model_year'] >= model_year_range[0]) & 
    (df['model_year'] <= model_year_range[1])
]

# Group data by model year and calculate average price
avg_price_by_year = filtered_df_model_year.groupby(['model_year'])['price'].mean().reset_index()

# Create and display the bar plot for model year comparison
fig6 = px.bar(
    avg_price_by_year,
    x='model_year',
    y='price',
    title=f'Average Price vs. Model Year for {dropdown_manufacturer} {dropdown_type}',
    labels={'price': 'Average Price (USD)', 'model_year': 'Model Year'}
)

# Update layout for better readability
fig6.update_layout(
    yaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1),
    xaxis=dict(showgrid=True, gridcolor='lightgray', gridwidth=1),
    plot_bgcolor='white',
    showlegend=False  # Only one manufacturer and type, so no need for a legend
)

# Display the bar plot for model year comparison
st.plotly_chart(fig6)

# Section: Average Price by Vehicle Type and Transmission
st.subheader('Average Price by Vehicle Type and Transmission')

# Get unique vehicle types and let the user select multiple types
dropdown_vehicle_types = st.multiselect('Select Vehicle Types', vehicle_types, default=[vehicle_types[0]])

# Filter data based on selected vehicle types
filtered_df_transmission = df[df['type'].isin(dropdown_vehicle_types)][['type', 'transmission', 'price']]

# Group by 'type' and 'transmission', and calculate the average price
avg_price_by_transmission = filtered_df_transmission.groupby(['type', 'transmission'])['price'].mean().reset_index()

# Create and display the bar plot for transmission comparison
fig7 = px.bar(
    avg_price_by_transmission,
    x='type',
    y='price',
    color='transmission',
    barmode='group',
    title='Average Price by Vehicle Type and Transmission Type',
    labels={'price': 'Average Price (USD)', 'type': 'Vehicle Type', 'transmission': 'Transmission'},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

# Update layout with hover effects, title, and gridlines
fig7.update_traces(
    hovertemplate='<b>%{x}</b><br>Transmission: %{marker.color}<br>Price: $%{y:,.0f}'
)
fig7.update_layout(
    title=dict(text='Average Price by Vehicle Type and Transmission Type', x=0.5, font=dict(size=20)),
    xaxis=dict(title='Vehicle Type', tickangle=-45, titlefont=dict(size=16), showgrid=False),
    yaxis=dict(title='Average Price (USD)', titlefont=dict(size=16), showgrid=True, gridcolor='lightgray', gridwidth=1),
    legend_title_text='Transmission Type',
    font=dict(size=12),
    plot_bgcolor='white'
)

# Display the transmission comparison plot
st.plotly_chart(fig7)
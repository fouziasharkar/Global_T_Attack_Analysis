import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#dataset
terror = pd.read_csv('terror2.csv')

terror['state'].drop_duplicates(inplace=True)
terror['state'].replace('Paktika Province','Paktika',inplace=True)

grouped_terror = terror.groupby(['country', 'state', 'date']).agg(
    total_kills=('fatalities', 'sum'),
    total_injuries=('injuries', 'sum'),
    latitude=('latitude', 'mean'),
    longitude=('longitude', 'mean')
).reset_index()

terror = terror[terror['state']!='Unknown']

terror['weapon'].replace('Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)','Vehicle',inplace=True)

terror['state'].replace(['Paktika Province', 'Fier (County)', 'Kukës (County)','Aïn Defla',r'^Batna.*',r'^Bejaia.*',
                         'Bordj Bou Arréridj',r'^Boumerdés.*'],
                        ['Paktika', 'Fier', 'Kukes','Aïn Defla (Province)','Batna(Province)',
                         'Bejaia(Province)','Bordj Bou Arreridj','Boumerdes Province']
                        , inplace=True)


#first selectbox
country_name = sorted(terror['country'].unique().tolist())
country_name.insert(0,'Select')
country_name.insert(1,'Global')

#to wide the streamlit width
st.set_page_config(layout='wide')

#sidebar title
st.sidebar.title('Global Terrorism Data Analysis (1970-2017)')

#first selectbox
selected_country = st.sidebar.selectbox('Select a country',country_name)

#plot graph button
btn1 = st.sidebar.button('Plot Graph')

if btn1:
    # Grouping the data
    if selected_country == 'Global':

        # Format the date in "19 April, 2015" style
        grouped_terror['formatted_date'] = pd.to_datetime(grouped_terror['date']).dt.strftime('%d %B, %Y')

        # Custom Red color scale
        red_scale = [(0, "lightcoral"), (0.5, "red"), (1, "darkred")]

        # Scatter mapbox plot
        fig = px.scatter_mapbox(
            grouped_terror,
            lat="latitude",
            lon="longitude",
            size="total_kills",  # Circle size based on total kills
            color="total_injuries",  # Circle color based on total injuries
            zoom=1,
            mapbox_style='carto-positron',
            size_max=40,
            width=1200, height=700,
            color_continuous_scale=red_scale,
            range_color=[1000, 50000],
            hover_data={
                'country': True,  # Display country in hover
                'state': True,  # Display state in hover
                'formatted_date': True,  # Display formatted date in hover
                'total_kills': True,  # Display total kills in hover
                'total_injuries': True  # Display total injuries in hover
            }
        )

        # Update hover template to remove default information and only show custom fields
        fig.update_traces(
            hovertemplate="<b>Country:</b> %{customdata[0]}<br>" +
                          "<b>State:</b> %{customdata[1]}<br>" +
                          "<b>Date:</b> %{customdata[2]}<br>" +
                          "<b>Total Kills:</b> %{customdata[3]}<br>" +
                          "<b>Total Injuries:</b> %{customdata[4]}<extra></extra>",
            hoverinfo="text",
            marker=dict(opacity=1)
        )

        # Update the layout with a title and hover label styling
        fig.update_layout(
            title={
                'text': "Total Kills and Injuries",
                'font': {
                    'size': 24,  # Set the font size to 24 (you can adjust this value as needed)
                    'family': "Arial"
                }
            },
            hoverlabel=dict(
                font_color="white",
                font_size=12,
                font_family="Arial",
                bgcolor="rgb(250, 99, 71)"  # Transparent background for hover
            )
        )

        #################################### Second fig ############################################


        # Aggregate total fatalities by year and country
        total_killings = terror.groupby(['year', 'country'], as_index=False)['fatalities'].sum()

        # Create an animated bar chart for total fatalities by country over the years
        fig1 = px.bar(
            total_killings,
            x='country',
            y='fatalities',
            color='country',
            log_y=True,
            animation_frame='year',
            #range_y=[0, total_killings['fatalities'].max() + 100],  # Adjust y-axis range
            title='Total Fatalities by Country Over the Years',
            labels={'fatalities': 'Total Fatalities'},
            width=1200,
            height=800,
            hover_data={'country': False}
        )

        fig1.update_layout(
            title={
                'text': "Total Fatalities by Country Over the Years",
                'font': {
                    'size': 24,  # Set the font size to 24 (you can adjust this value as needed)
                    'family': "Arial"
                }}
            ,xaxis_title='',
            hoverlabel=dict(
                font_color="white",
                font_size=12,
                font_family="Arial",
                bordercolor="white",
                bgcolor="rgb(255, 187, 0)"  # Transparent background for hover
            )        
        )

        ########################################## third fig ####################################


        # Group the data by weapon and sum the fatalities
        global_weapon_data = terror.groupby('weapon', as_index=False)['fatalities'].sum()

        # Create a bubble plot for global weapon data
        fig3 = px.scatter(
            global_weapon_data,
            x='weapon',
            y='fatalities',
            log_y = True,
            size='fatalities',
            color='weapon',
            title='Weapon Used Globally For Attacks',
            labels={'fatalities': 'Total Fatalities'},
            hover_name='weapon',  # Show weapon name on hover
            size_max=60,  # Max size for bubbles
            width =1200,
            height= 550
        )

        # Update layout for better appearance
        fig3.update_layout(
            title_font=dict(size=24),  # Increase title font size
            xaxis_title='Weapon',
            yaxis_title='Total Fatalities',
            xaxis_tickangle=-45,
        )

    st.plotly_chart(fig,use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

else:
    # Filter the dataset for the selected country
    each_country = grouped_terror[grouped_terror['country'] == selected_country]

    # Format the date in "19 April, 2015" style
    each_country['formatted_date'] = pd.to_datetime(each_country['date']).dt.strftime('%d %B, %Y')

    # Custom Red color scale
    red_scale = [(0, "lightcoral"), (0.5, "red"), (1, "darkred")]

    # Scatter mapbox plot
    fig = px.scatter_mapbox(
        each_country,
        lat="latitude",
        lon="longitude",
        size="total_kills",  # Circle size based on total kills
        color="total_injuries",  # Circle color based on total injuries
        zoom=3,  # Adjust zoom level for better country-specific view
        mapbox_style='carto-positron',
        size_max=40,
        width=1200, height=700,
        color_continuous_scale=red_scale,
        range_color=[0, each_country['total_injuries'].max()],  # Adjust color range based on data
        hover_data={
            #'country': False,  # Display country in hover
            'state': True,  # Display state in hover
            'formatted_date': True,  # Display formatted date in hover
            'total_kills': True,  # Display total kills in hover
            'total_injuries': True  # Display total injuries in hover
        }
    )

    # Update hover template to remove default information and show only custom fields
    fig.update_traces(
        hovertemplate= #"<b>Country:</b> %{customdata[0]}<br>" +  # Display country
                      "<b>State:</b> %{customdata[0]}<br>" +  # Display state
                      "<b>Date:</b> %{customdata[1]}<br>" +  # Display formatted date
                      "<b>Total Kills:</b> %{customdata[2]}<br>" +  # Display total kills
                      "<b>Total Injuries:</b> %{customdata[3]}<br>",  # Display total injuries
        hoverinfo="text",
        marker=dict(opacity=1)
    )

    # Update the layout with a title and hover label styling
    fig.update_layout(
        title={
            'text': f"Total Kills and Injuries in {selected_country}",  # Dynamic country name in title
            'font': {
                'size': 24,  # Set font size to 24
                'family': "Arial"
            }
        },
        hoverlabel=dict(
            font_color="white",
            font_size=12,
            font_family="Arial",
            bgcolor="rgb(250, 99, 71)"  # Transparent background for hover
        )
    )


    ########################################### Second fig (bar)##################################################

    # Filter the DataFrame for the selected country
    filtered_data = terror[terror['country'] == selected_country]

    # Define year ranges and corresponding labels
    year_ranges = {
        '1970-1980': (1970, 1980),
        '1981-1990': (1981, 1990),
        '1991-2000': (1991, 2000),
        '2001-2010': (2001, 2010),
        '2011-2017': (2011, 2017)
    }

    # Create a mapping of years to year ranges
    filtered_data['year_range'] = pd.cut(
        filtered_data['year'],
        bins=[1969, 1980, 1990, 2000, 2010, 2017],
        labels=list(year_ranges.keys()),
        right=True
    )

    # Group by state and year_range to sum up fatalities
    grouped_data = filtered_data.groupby(['state', 'year_range'], as_index=False)['fatalities'].sum()

    # Create a color map for year ranges
    color_map = {
        '1970-1980': 'blue',
        '1981-1990': 'orange',
        '1991-2000': 'green',
        '2001-2010': 'red',
        '2011-2017': 'purple'
    }

    # Create a grouped bar chart with distinct colors for year ranges
    fig1 = px.bar(
        grouped_data,
        x='state',
        y='fatalities',
        log_y=True,
        color='year_range',  # Color bars by year range
        color_discrete_sequence=list(color_map.values()),  # Set custom colors for each year range
        barmode='stack',  # Group bars together
        title=f'Total Fatalities by State in {selected_country} Over Years',
        labels={'fatalities': 'Total Fatalities'},
    )

    # Customize hover data to show year range correctly
    fig1.update_traces(
        hovertemplate="<b>Year Range:</b> %{customdata[0]}<br>" +  # Display year range from custom data
                      "<b>Total Fatalities:</b> %{y:.0f}<br>" +  # Show total fatalities
                      "<extra></extra>",  # Remove additional hover information
        customdata=grouped_data[['year_range']].values  # Include year range in custom data
    )

    # Update layout for better appearance
    fig1.update_layout(
        height=600,
        title_font=dict(size=24),  # Increase title font size
        xaxis_title='States',
        yaxis_title='Total Fatalities',
        xaxis_tickangle=-45,
    )

    #################################### Third fig ############################################

    # Filter the DataFrame for the selected country
    filtered_country_data = terror[terror['country'] == selected_country]

    # Group the data by weapon and sum the fatalities for the selected country
    country_weapon_data = filtered_country_data.groupby('weapon', as_index=False)['fatalities'].sum()

    # Create a bubble plot for the country's weapon data
    fig2 = px.scatter(
        country_weapon_data,
        x='weapon',
        y='fatalities',
        log_y =True,
        size='fatalities',
        color='weapon',
        title=f'Weapons Used in {selected_country} for Attacks ',
        labels={'fatalities': 'Total Fatalities'},
        hover_name='weapon',  # Show weapon name on hover
        size_max=70,  # Max size for bubbles
        width=1200,
        height=550
    )

    # Update layout for better appearance
    fig2.update_layout(
        title_font=dict(size=24),  # Increase title font size
        xaxis_title='Weapon',
        yaxis_title='Total Fatalities',
        xaxis_tickangle=-45,
    )


    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

























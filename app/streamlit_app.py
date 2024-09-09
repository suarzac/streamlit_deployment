from collections import namedtuple
import math
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px


# Page configuration
st.set_page_config(
    page_title="Suarez's Dash",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Sidebar
with st.sidebar:
    st.title('My Dash')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    file_path = 'sources/Chase Activity Jan 1 to Aug 23.CSV'
    df = pd.read_csv(file_path)
    
    category_list = list(df.Category.unique())
    
    selected_category = st.selectbox('Select a category', category_list)
    df_selected_category = df[df.Category == selected_category]
    df_selected_category_sorted = df_selected_category.sort_values(by="Amount", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)



# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Amount", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year.population)),
                               scope="usa",
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)

def calculate_amount_date(input_df, input_category):
  selected_year_data = input_df[input_df['Category'] == input_category].reset_index()
  previous_year_data = input_df[input_df['Category'] == input_category - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)



# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Gains/Losses')

   #  df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)
   #  df_category_amount_sorted = calculate_amount_date(df, selected_category)

   #  if selected_year > 2010:
   #      first_state_name = df_population_difference_sorted.states.iloc[0]
   #      first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
   #      first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
   #  else:
   #      first_state_name = '-'
   #      first_state_population = '-'
   #      first_state_delta = ''
   #  st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

   #  if selected_year > 2010:
   #      last_state_name = df_population_difference_sorted.states.iloc[-1]
   #      last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
   #      last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
   #  else:
   #      last_state_name = '-'
   #      last_state_population = '-'
   #      last_state_delta = ''
   #  st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

    
   #  st.markdown('#### States Migration')

   #  if selected_year > 2010:
   #      # Filter states with population difference > 50000
   #      # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
   #      df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference > 50000]
   #      df_less_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference < -50000]
        
   #      # % of States with population difference > 50000
   #      states_migration_greater = round((len(df_greater_50000)/df_population_difference_sorted.states.nunique())*100)
   #      states_migration_less = round((len(df_less_50000)/df_population_difference_sorted.states.nunique())*100)
   #      donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
   #      donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')
   #  else:
   #      states_migration_greater = 0
   #      states_migration_less = 0
   #      donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
   #      donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')

   #  migrations_col = st.columns((0.2, 1, 0.2))
   #  with migrations_col[1]:
   #      st.write('Inbound')
   #      st.altair_chart(donut_chart_greater)
   #      st.write('Outbound')
   #      st.altair_chart(donut_chart_less)

with col[1]:
    st.markdown('#### Heatmap')
    
    heatmap = make_heatmap(df, 'Amount', 'Transaction Date', 'Category', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)
    
with col[2]:
    st.markdown('#### Top States')

    st.dataframe(df_selected_category_sorted,
                 column_order=("Description", "Categoy", "Amount"),
                 hide_index=True,
                 width=None,
               #   column_config={
               #      "states": st.column_config.TextColumn(
               #          "States",
               #      ),
               #      "population": st.column_config.ProgressColumn(
               #          "Population",
               #          format="%f",
               #          min_value=0,
               #          max_value=max(df_selected_category_sorted.population),
               #       )}
                 )
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
            - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
            - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
            ''')
        


with st.echo(code_location='below'):
   
   df.fillna(0, inplace=True)
   df = df[df['Category'] == selected_category]

   df['Transaction Date'] = df['Transaction Date'].astype('datetime64[ns]')
   grouped_df = df.groupby(['Category', 'Transaction Date'])['Amount'].sum().reset_index()
   st.dataframe(grouped_df,
                 column_order=("Category", "Transaction Date", "Amount"),
                 hide_index=True,
                 width=None,
               #   column_config={
               #      "states": st.column_config.TextColumn(
               #          "States",
               #      ),
               #      "population": st.column_config.ProgressColumn(
               #          "Population",
               #          format="%f",
               #          min_value=0,
               #          max_value=max(df_selected_year_sorted.population),
               #       )}
               )
   st.write(df)
   st.write(grouped_df)

   # st.altair_chart(alt.Chart(df, height=500, width=500)
   #    .mark_circle(color='#0068c9', opacity=0.5)
   #    .encode(x='x:Q', y='y:Q'))

with st.echo(code_location='below'):
   total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
   num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

   Point = namedtuple('Point', 'x y')
   data = []

   points_per_turn = total_points / num_turns

   for curr_point_num in range(total_points):
      curr_turn, i = divmod(curr_point_num, points_per_turn)
      angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
      radius = curr_point_num / total_points
      x = radius * math.cos(angle)
      y = radius * math.sin(angle)
      data.append(Point(x, y))

   st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
      .mark_circle(color='#0068c9', opacity=0.5)
      .encode(x='x:Q', y='y:Q'))
   

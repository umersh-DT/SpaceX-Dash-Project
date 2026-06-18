import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# 1. Load data from your exact file path
file_path = r"C:\Users\umers\Downloads\spaceY project\spacex_launch_geo.csv"
spacex_df = pd.read_csv(file_path)

# Build the missing version category column safely
spacex_df['Booster Version Category'] = spacex_df['Booster Version'].apply(lambda x: ' '.join(str(x).split()[:2]))

# Define the limits directly from your dataset columns
min_payload = float(spacex_df['Payload Mass (kg)'].min())
max_payload = float(spacex_df['Payload Mass (kg)'].max())

# 2. Initialize the app
app = dash.Dash(__name__)

# 3. App Layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[0, 10000] # Force handles to start fully loaded
    ),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2 Callback: Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        df_counts = site_df['class'].value_counts().reset_index()
        df_counts.columns = ['class', 'count']
        fig = px.pie(df_counts, values='count', names='class', title=f'Total Success Launches for site {entered_site}')
    return fig

# TASK 4 Callback: Completely Simplified to Force Display
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    # Fallback bounds protection
    low = float(payload_range[0]) if payload_range else 0.0
    high = float(payload_range[1]) if payload_range else 10000.0
    
    # 1. Filter by slider range on the entire dataset first
    mask = (spacex_df['Payload Mass (kg)'].astype(float) >= low) & (spacex_df['Payload Mass (kg)'].astype(float) <= high)
    filtered_df = spacex_df[mask]
    
    # 2. Filter by site selection
    if entered_site and entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        title_text = f'Correlation for site {entered_site}'
    else:
        title_text = 'Correlation between Payload and Success for all Sites'
        
    # 3. Create chart completely clean
    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class',
        color='Booster Version Category',
        title=title_text
    )
    return fig

# 4. Run the app on a clean, alternate network port (8060) to avoid session cache
if __name__ == '__main__':
    app.run(port=8060)
    

from datetime import datetime
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
from collections import defaultdict
import json

def calculate_party_legislation(raw_members):
    all_time_counts = defaultdict(int)
    for r_member in raw_members:
        if r_member.get("sponsored_legislation_count") is not None:
            all_time_counts[r_member.get("party")] += r_member.get("sponsored_legislation_count")
    return all_time_counts

def calculate_state_legislation(raw_members):
    all_time_counts = defaultdict(int)
    for r_member in raw_members:
        if r_member.get("sponsored_legislation_count") is not None:
            all_time_counts[r_member.get("state")] += r_member.get("sponsored_legislation_count")
    return all_time_counts

def calculate_ages(raw_members):
    avg_age_by_state_at_start_lists = defaultdict(list)
    for r_member in raw_members:
        age = int(r_member.get("year_of_first_term")) - int(r_member.get("birth_year"))
        avg_age_by_state_at_start_lists[r_member.get("state")].append(age)

    avg_age_by_state_at_start = {}
    for state in avg_age_by_state_at_start_lists:
        avg_age_by_state_at_start[state] = sum(avg_age_by_state_at_start_lists[state]) / len(avg_age_by_state_at_start_lists[state])
    return avg_age_by_state_at_start

def display_party_legislation_plot(legislation_by_party):
    # Create a pie chart
    fig = go.Figure(
        data=[go.Pie(labels=list(legislation_by_party.keys()), values=list(legislation_by_party.values()))],
    )

    # Set the chart title and layout
    fig.update_layout(
        title="Number of Pieces of Legislation by Party",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Show the chart
    fig.show()

    # Convert the chart to HTML
    html = pio.to_html(fig, full_html=False)

    # Print the HTML code
    print(html)


def display_state_legislation_plot(legislation_by_state):
    # Define the color scale
    color_scale = [
        [0.0, "rgb(255,255,255)"],
        [0.2, "rgb(255,215,215)"],
        [0.4, "rgb(255,165,165)"],
        [0.6, "rgb(255,100,100)"],
        [0.8, "rgb(255,50,50)"],
        [1.0, "rgb(255,0,0)"],
    ]

    # Create the map trace
    map_trace = go.Choropleth(
        locations=list(legislation_by_state.keys()),
        z=list(legislation_by_state.values()),
        locationmode="USA-states",
        colorscale=color_scale,
        colorbar_title="Value",
    )

    # Define the layout
    layout = go.Layout(
        title="Legislation by State",
        geo=dict(scope="usa", projection=dict(type="albers usa"), showlakes=False),
    )

    # Create the figure and add the trace and layout
    fig = go.Figure(data=[map_trace], layout=layout)

    # Show the figure
    fig.show()


if __name__ == "__main__":
    with open("../../sample_data/members_with_details.json") as f:
        raw = json.loads(f.read())
        b = calculate_party_legislation(raw)
        b2 = calculate_party_legislation(raw)
        b3 = calculate_ages(raw)
    display_party_legislation_plot(b)
    display_state_legislation_plot(b2)
    display_state_legislation_plot(b3)

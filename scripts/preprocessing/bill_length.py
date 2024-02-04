from datetime import datetime
import plotly.graph_objs as go
import pandas as pd
import json

def calculate_bill_lengths(raw_bills):
    bills = []
    for r_bill in raw_bills:
        bills.append({
            "title": r_bill["title"],
            "congress": r_bill["congress"],
            "bill_number": r_bill["bill_number"],
            "length": (datetime.strptime(r_bill["latest_action_date"], "%Y-%m-%d") - datetime.strptime(r_bill["introduced_date"], "%Y-%m-%d")).days
        })
    return bills

def display_plot(bills):
    fig = go.Figure(data=go.Scatter(x=bills["length"],
                                    y=bills.index,
                                    mode="markers",
                                    marker=dict(size=10, color=bills.index),
                                    text=bills["title"] + '<br>' +
                                        'Congress: ' + bills["congress"] + '<br>' +
                                        'Bill Number: ' + bills["bill_number"],
                                    hovertemplate='%{text}<extra></extra>'))

    fig.update_layout(title='Time Taken for US Legislation to Pass',
                    xaxis_title='Time to Pass (in days)',
                    yaxis_title='Bill Number',
                    template='plotly_dark')

    fig.show()

if __name__ == "__main__":
    with open("../../sample_data/bills_with_details.json") as f:
        b = calculate_bill_lengths(json.loads(f.read()))
    display_plot(pd.read_json(json.dumps(b)))

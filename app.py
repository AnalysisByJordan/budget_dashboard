
import pandas as pd
import random as random
import datetime as datetime
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# In[2]:


dates = [2018,2019,2020,2021]


# In[3]:


categories = ["Reoccuring Bills", "Shopping", "Education", "Entertainment", "Services", "Misc."]
sub_categories = ['Hobbies','Professional Course','Bills','Subscriptions','Groceries','Restaurant/Bar',
'Car Repair','Gas','Clothing','Personal Care','Self Improvement','Tools/Appliances','Technology', 'Utilities']
primary_input_category = ['Salary']
aux_input_category = ['Gift', 'Windfall']
input_source = ["Employer"]
aux_input_source = ['Other']


# In[4]:


def outputGenerator(dates):
    date_list = []
    category_list = []
    sub_category_list = []
    for date in dates:
        start_date = datetime.date(date, 1, 1)
        end_date = datetime.date(date, 12, 31)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        for i in range(200):
            random_number_of_days = random.randrange(days_between_dates)
            random_date = start_date + datetime.timedelta(days=random_number_of_days)
            date_list.append(random_date)
            category_list.append(random.choice(categories))
            sub_category_list.append(random.choice(sub_categories))
    date_list.sort()
    year_total = random.randint(30000,60000)
    random_range_begin = random.randint(40000,45000)
    random_range_end = random.randint(1500000,6500000)
    amount_list = [random.randint(random_range_begin,random_range_end) for i in range(1,800)]
    amount_list = [ round(i/year_total) for i in amount_list ]
    output_df = pd.DataFrame(list(zip(date_list, category_list, sub_category_list, amount_list)), columns = ['Date', 'Category', 'Sub-Category','Amount'])
    output_df['Year'] = list(map(lambda x: x.year, output_df.Date))
    output_df['Month'] = list(map(lambda x: x.strftime("%b"), output_df.Date))
    return(output_df)


# In[5]:


def inputGenerator(dates):
    input_date_list = []
    input_category_list = []
    input_source_list = []
    input_amount_list = []
    for date in dates:
        input_year_total = random.randint(55000,65000)
        paycheck = input_year_total / 26
        start_date = datetime.date(date, 1, 1)
        for i in range(0,26):
            input_date_list.append(start_date)
            input_category_list.append(random.choice(primary_input_category))
            input_source_list.append(random.choice(input_source))
            input_amount_list.append(round(paycheck))
            if random.randint(1,10) == 1:
                input_date_list.append(start_date)
                input_category_list.append(random.choice(aux_input_category))
                input_source_list.append(random.choice(aux_input_source))
                input_amount_list.append(round(random.randint(100,1000)))
            start_date = start_date + datetime.timedelta(days=14)
    input_date_list.sort()
    input_df = pd.DataFrame(list(zip(input_date_list, input_category_list, input_source_list, input_amount_list)), columns = ['Date', 'Input Category', 'Source','Amount'])
    input_df['Year'] = list(map(lambda x: x.year, input_df.Date))
    input_df['Month'] = list(map(lambda x: x.strftime("%b"), input_df.Date))
    return(input_df)


# In[6]:


output_df = outputGenerator(dates) #pd.read_excel('budget.xlsx', sheet_name = 'Ouput')
output_df


# In[7]:


input_df = inputGenerator(dates) #pd.read_excel('budget.xlsx', sheet_name = 'Input')
input_df


# In[8]:


def yearSelect(year):
    func_df = output_df[output_df['Year'] == year]
    output_category_sum = pd.DataFrame(func_df.groupby(['Category','Month']).Amount.sum()).reset_index()
    output_subcategory_sum = pd.DataFrame(func_df.groupby(['Sub-Category','Month']).Amount.sum()).reset_index()
    output_sum = pd.DataFrame(func_df.groupby(['Month']).Amount.sum()).reset_index()
    output_category_fig = px.bar(output_category_sum, x = "Month", y = "Amount", color = 'Category',
                                category_orders= {"Month" : list(func_df.Month.unique())})
    output_category_fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', font_color="#45A29E",)
    output_subcategory_fig = px.bar(output_subcategory_sum, x = "Month", y = "Amount", color = "Sub-Category",
                                   category_orders= {"Month" : list(func_df.Month.unique())})
    output_subcategory_fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', font_color="#45A29E",)
    output_sum_fig = px.bar(output_sum, x = "Month", y = "Amount", color_discrete_sequence =['red']*3,
                           category_orders= {"Month" : list(func_df.Month.unique())})
    output_sum_fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', font_color="#45A29E",)
    graph_list = [output_category_fig, output_subcategory_fig, output_sum_fig]
    return(graph_list)



# In[9]:


def inputSelect(year):
    func_df = input_df[input_df['Year'] == year]
    input_category_sum = pd.DataFrame(func_df.groupby(['Input Category','Month']).Amount.sum()).reset_index()
    input_sum = pd.DataFrame(func_df.groupby(['Month']).Amount.sum()).reset_index()
    input_category_fig = px.bar(input_category_sum, x = "Month", y = "Amount", color = "Input Category",
                               category_orders= {"Month" : list(func_df.Month.unique())})
    input_category_fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', font_color="#45A29E",)
    input_sum_fig = px.bar(input_sum, x = "Month", y = "Amount", color_discrete_sequence =['green']*3,
                          category_orders= {"Month" : list(func_df.Month.unique())})
    input_sum_fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', font_color="#45A29E",)
    graph_list = [input_category_fig, input_sum_fig]
    return(graph_list)



# In[10]:


def diffSelect(year):
    input_func_df = input_df[input_df['Year'] == year]
    output_func_df = output_df[output_df['Year'] == year]
    input_sum = pd.DataFrame(input_func_df.groupby(['Month']).Amount.sum()).reset_index()
    output_sum = pd.DataFrame(output_func_df.groupby(['Month']).Amount.sum()).reset_index()
    total_df = input_sum.rename(columns={'Amount':'Input_Total'})
    total_df['Output_Total'] = list(map(lambda x: x*-1, output_sum.Amount))
    total_df['Total'] = total_df['Input_Total'] + total_df['Output_Total']
    total_fig = px.bar(total_df, x = "Month", y = "Total", category_orders= {"Month" : list(input_func_df.Month.unique())})
    total_fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)', font_color="#45A29E", )
    return(total_fig)



# In[11]:


def outputMetrics(year):
    output_func_df = output_df[output_df['Year'] == year]
    input_func_df = input_df[input_df['Year'] == year]
    
    output_sum = pd.DataFrame(output_func_df.groupby(['Month']).Amount.sum()).reset_index()
    output_category_sum = pd.DataFrame(output_func_df.groupby(['Category']).Amount.sum()).reset_index()
    output_subcategory_sum = pd.DataFrame(output_func_df.groupby(['Sub-Category']).Amount.sum()).reset_index()
    
    input_sum = pd.DataFrame(input_func_df.groupby(['Month']).Amount.sum()).reset_index()
    input_category_sum = pd.DataFrame(input_func_df.groupby(['Input Category']).Amount.sum()).reset_index()
    
    total_df = input_sum.rename(columns={'Amount':'Input_Total'})
    total_df['Output_Total'] = list(map(lambda x: x*-1, output_sum.Amount))
    total_df['Total'] = total_df['Input_Total'] + total_df['Output_Total']
    
    avg_spend = "$" + str(round(output_sum.Amount.mean()))
    biggest_spend_month = str(output_sum[output_sum["Amount"] == output_sum.Amount.max()].iloc[0]['Month']) + "($" + str(round(output_sum.Amount.max())) + ")"
    biggest_spend_category = output_category_sum[output_category_sum["Amount"] == output_category_sum.Amount.max()].Category.iloc[0]
    biggest_spend_subcategory = output_subcategory_sum[output_subcategory_sum["Amount"] == output_subcategory_sum.Amount.max()]["Sub-Category"].iloc[0]
    
    avg_income = "$" + str(round(input_sum.Amount.mean()))
    biggest_income_month = str(input_sum[input_sum["Amount"] == input_sum.Amount.max()].iloc[0]['Month']) + "($" + str(round(input_sum.Amount.max())) + ")"
    biggest_income_category = input_category_sum[input_category_sum["Amount"] == input_category_sum.Amount.max()]["Input Category"].iloc[0]
    
    avg_savings = "$" + str(round(total_df.Total.mean()))
    biggest_savings_month = str(total_df[total_df["Total"] == total_df.Total.max()].iloc[0]['Month']) + "($" + str(round(total_df.Total.max())) + ")"
    return({"Average Monthly Spend: " : avg_spend, "Highest Spending Month: " : biggest_spend_month, 
            "Biggest Spend Category: ": biggest_spend_category, "Biggest Spend Sub-Category: ": biggest_spend_subcategory,
            "Average Monthly Income: ": avg_income, "Biggest Income Month: ": biggest_income_month,
            "Biggest Income Category: ": biggest_income_category, "Average Savings: ": avg_savings,
            "Biggest Savings Month: ": biggest_savings_month
           })


# In[12]:


year_items = input_df.Year.unique()


# In[13]:

app = dash.Dash(__name__)
app.layout = html.Div(className = "full-page", children = [
    html.Div(className = "header", children = [
        html.Div(className = "header-text", children = [
            html.H1("Budget Analytics", className = "page-title"),
            html.P('''"True wealth is built when your monthly assets produce income 
                   that is greater than your monthly expenses"''', className = "page-quote"),
            html.Button("*RANDOMLY GENERATED BUDGET*", id = "generate", className = "generate-button")
        ])
    ]),
    html.Div(className = "all-graphs", children = [
        html.Div(className = "left-section", children = [
            html.Div(className = "output-section", children = [
                html.H1("Expenses", className = "expense-title"),
                html.Div(className = "dropdown-bar", children = [
                    html.Div(className = "dropdown-year", children = [
                        html.Div("Choose a year:", className = "year-label"),
                        dcc.Dropdown(
                            id = "selectYear",
                            options = [{'label': k, 'value': k} for k in year_items],
                            value = 2020
                            ),
                    ]),
                    html.Div(className = "middle-bar"),
                    html.Div(className = "dropdown-level", children = [
                        html.Div("Choose level of detail:", className = "year-label"),
                        dcc.Dropdown(
                            id='level-dropdown', 
                            options=[
                                {'label': 'Total', 'value': 'Total'},
                                {'label': 'Category', 'value': 'Category'},
                                {'label': 'Sub-Category', 'value': 'Sub-Category'}],
                            value = 'Total'),                   
                    ])
                ]),
   
                html.Div(className = "graph-house", children = [
                    dcc.Graph(        
                        id = "outputFigure",
                        style={'height': '100%', 'width': '100%', "margin" : "dict(l=0,r=0,b=0,t=0)", 
                               "paper_bgcolor":'rgba(0,0,0,0)',
                                "plot_bgcolor":'rgba(0,0,0,0)'},
                        config={
                        'responsive': True, # Doesn't seem to help
                        'displayModeBar': False})
                ]),

            ]),
            html.Div(className = "middle-section"),
            html.Div(className = "input-section", children = [
                html.H1("Income", className = "income-title"),
                    html.Div(className = "dropdown-bar", children = [
                        html.Div(className = "dropdown-year", children = [
                            html.Div("Choose a year:", className = "year-label"),
                            dcc.Dropdown(
                                id = "selectYearInput",
                                options = [{'label': k, 'value': k} for k in year_items],
                                value = 2020
                                ),
                            ]),
                        html.Div(className = "middle-bar"),
                        html.Div(className = "dropdown-level", children = [
                            html.Div("Choose level of detail:", className = "year-label"),
                            dcc.Dropdown(
                                id='input-level-dropdown', 
                                options=[
                                    {'label': 'Total', 'value': 'Total'},
                                    {'label': 'Category', 'value': 'Category'}],
                                value = 'Total'),
                            ])
                    ]),
                html.Div(className = "graph-house", children = [
                    dcc.Graph(
                        id = "inputFigure", 
                        style={'height': '100%', 'width': '100%', "margin" : "dict(l=0,r=0,b=0,t=0)", 
                               "paper_bgcolor":'rgba(0,0,0,0)',
                                "plot_bgcolor":'rgba(0,0,0,0)'},
                        config={
                        'responsive': True, # Doesn't seem to help
                        'displayModeBar': False})
                ]),
                ])

            ]),
            html.Div(className = "right-section", children = [
                html.Div(className = "difference-section", children = [
                    html.H1("Net Savings", className = "savings-title"),
                    html.Div(className = "dropdown-bar", children = [
                        html.Div(className = "dropdown-year", children = [
                            html.Div("Choose a year:", className = "year-label"),
                            dcc.Dropdown(
                                id = "selectYearDiff",
                                options = [{'label': k, 'value': k} for k in year_items],
                                value = 2020
                                ),
                            ]),
                        html.Div(className = "middle-bar"),
                        html.Div(className = "dropdown-level")
                    ]),                        
                    html.Div(className = "graph-house", children = [
                        dcc.Graph(
                            id = "diffFigure",
                            style={'height': '100%', 'width': '100%', "margin" : "dict(l=0,r=0,b=0,t=0)",
                               "paper_bgcolor":'rgba(0,0,0,0)',
                                "plot_bgcolor":'rgba(0,0,0,0)'},
                            config={
                                'responsive': True, # Doesn't seem to help
                                'displayModeBar': False})
                    ]),
                ]),
                html.Div(className = "middle-section"),
                html.Div(className = "metrics-section", children = [
                    html.H1("Metrics", className = "metrics-title"),
                    html.Div(className = "dropdown-bar", children = [
                        html.Div(className = "dropdown-year", children = [
                            html.Div("Choose a year:", className = "year-label"),
                            dcc.Dropdown(
                                id = "selectYearMetrics",
                                options = [{'label': k, 'value': k} for k in year_items],
                                value = 2020
                                ),
                            ]),
                        html.Div(className = "middle-bar"),
                        html.Div(className = "dropdown-level")
                    ]),
                    html.Div(className = "metrics-box", children = [
                        html.Div(className = "stats", children = [
                            html.Div(className = "stats-left", children = [
                                html.Div(className = "metric-div", children = [
                                    html.P("Average Monthly Spend: ", className = "metric-statement"),
                                    html.P(id = "average-monthly",className = "metric-answer")
                                ]),
                                html.Div(className = "metric-div", children = [
                                    html.P("Highest Spending Month: ", className = "metric-statement"),
                                    html.P(id = "highest_spending", className = "metric-answer")
                                ]),
                                html.Div(className = "metric-div", children = [
                                    html.P("Biggest Spend Category: ", className = "metric-statement"),
                                    html.P(id = "biggest_spending", className = "metric-answer")
                                ]),
                                html.Div(className = "metric-div", children = [
                                    html.P("Biggest Spend Sub-Category: ", className = "metric-statement"),
                                    html.P(id = "biggest_spending_sub", className = "metric-answer")
                                ]),
                                html.Div(className = "metric-div", children = [
                                    html.P("Average Monthly Income: ", className = "metric-statement"),
                                    html.P(id = "average-income", className = "metric-answer")
                                ]),
                            ]),
                            html.Div(className = "stats-middle"),
                            html.Div(className = "stats-right", children = [
                                html.Div(className = "metric-div", children = [
                                    html.P("Biggest Income Month: ", className = "metric-statement"),
                                    html.P(id = "biggest-income", className = "metric-answer")
                                ]),
                                html.Div(className = "metric-div", children = [
                                    html.P("Biggest Income Category: ", className = "metric-statement"),
                                    html.P(id = "biggest-income-cat", className = "metric-answer")
                                ]),
                                html.Div(className = "metric-div", children = [
                                    html.P("Average Savings: ", className = "metric-statement"),
                                    html.P(id = "average_saving", className = "metric-answer")
                                ]),
                                html.Div(className = "metric-div", children = [
                                    html.P("Biggest Savings Month: ", className = "metric-statement"),
                                    html.P(id = "biggest-savings", className = "metric-answer")
                                ]),
                            ]),
                        ])
                    ])
                ])
            ]),
    ])
])
# ------------------------------------------------------Callbacks ------------------------------------------------------
# call to randomly generate a budget------------

# callback to update output graph----------------
@app.callback(
    Output("outputFigure", "figure"),[
        Input("selectYear", "value"),
        Input("level-dropdown", "value")
    ]
)
def detailYear(year, level):
    number = 0
    if level == "Category":
        number = 0
    elif level == "Sub-Category":
        number = 1
    elif level == "Total":
        number = 2
    return(yearSelect(year)[number])

# callback to update input graph-----------------
@app.callback(
    Output("inputFigure", "figure"),[
        Input("selectYearInput", "value"),
        Input("input-level-dropdown", "value")
    ]
)
def inputGraphChange(year, level):
    number = 0
    if level == "Category":
        number = 0
    elif level == "Total":
        number = 1
    return(inputSelect(year)[number])

#callback to update diff graph--------------------
@app.callback(
    Output("diffFigure", "figure"),[
        Input("selectYearDiff", "value")
    ]
)
def diffGraphChange(year):
    return(diffSelect(year))

#callback to update metrics-------------------------
@app.callback(
    Output('average-monthly', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Average Monthly Spend: "))

@app.callback(
    Output('highest_spending', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Highest Spending Month: "))

@app.callback(
    Output('biggest_spending', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Biggest Spend Category: "))

@app.callback(
    Output('biggest_spending_sub', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Biggest Spend Sub-Category: "))

@app.callback(
    Output('average-income', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Average Monthly Income: "))

@app.callback(
    Output('biggest-income', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Biggest Income Month: "))

@app.callback(
    Output('biggest-income-cat', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Biggest Income Category: "))

@app.callback(
    Output('average_saving', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Average Savings: "))

@app.callback(
    Output('biggest-savings', 'children'),
    [Input('selectYearMetrics', 'value'),]
)
def metricChange(year):
    return(outputMetrics(year).get("Biggest Savings Month: "))

# Run app and display result inline in the notebook
if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:





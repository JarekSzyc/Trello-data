from trello import TrelloClient
import pandas as pd
import matplotlib.pyplot as plt

def client_init(direc_key, direc_token):
    '''
    '''
    with open(direc_key) as key:
        api_key = key.read()
    with open(direc_token) as tok:
        token = tok.read()

    client = TrelloClient(
        api_key=api_key,
        token=token)

    return client

def get_dataframe(cards):
    '''
    '''
    data_dict = {}
    for i,card in enumerate(cards):
        data_dict[i] = {'Name': card.name, 'Date': card.due_date, 'Labels': card.labels}

    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df = df.sort_values('Date')

    return df

def get_time_series(df):
    '''
    '''
    series = df['Name'].groupby(by=df['Date'].dt.date).count().reset_index(name='count')
    series.set_index('Date', drop=True, inplace=True)
    return series

def plot_MA(series, MA=[7], fontsize=14, figsize=(13,6), title='Number of Trello Cards completed per day - Moving Average', tit_size=20):
    '''
    '''
    plt.rcParams.update({'font.size': fontsize})
    fig = plt.figure(figsize=figsize)
    for item in MA:
        plt.plot(series.rolling(item).mean(), label=f'MA({item})')
    plt.grid()
    plt.legend()
    plt.title(title, fontsize=tit_size);
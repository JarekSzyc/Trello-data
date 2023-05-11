from trello import TrelloClient
import pandas as pd
import matplotlib.pyplot as plt

def client_init(the_api_key, the_token, from_file=True):
    """ Initialization of Trello API client

    Parameters
    ----------
    the_api_key: str
        Name of the text file with user api key or the api key itself (depending on from_file param)
    the_token: str
        Name of the text file with user api key or the api key itself (depending on from_file param)
    from_file: bool
        if True, previous params are supposed to be names of files containing trello credentials

    Returns
    -------
    trello.trelloclient.TrelloClient object

    Note
    -------
    How to get Trello credentials:
        https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/

    """
    if from_file:
        with open(the_api_key) as key:
            api_key = key.read()
        with open(the_token) as tok:
            token = tok.read()
    else:
        api_key = the_api_key
        token = the_token

    client = TrelloClient(
        api_key=api_key,
        token=token)

    return client

def get_dataframe(cards):
    """ Obtain a dataframe with information from the cards

    We are interested in certain attributes of cards, namely:
        - card name
        - due date (when task was finished)
        - labels assigned

    Parameters
    ----------
    cards: list of trello.card.Card objects
        list obtained from Board using .get_cards() method

    Returns
    -------
    pandas Dataframe
        table with card names, dates and card labels

    """
    data_dict = {}
    for i,card in enumerate(cards):
        data_dict[i] = {'Name': card.name, 'Date': card.due_date, 'Labels': card.labels}

    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    df = df.sort_values('Date')

    return df

def get_time_series(df):
    """ Count how many cards were completed each day

    Parameters
    ----------
    df: pandas Dataframe
        output of get_dataframe function

    Returns
    -------
    pandas data series
        date as an index and number of completed tasks as values

    """
    series = df['Name'].groupby(by=df['Date'].dt.date).count().reset_index(name='count')
    series.set_index('Date', drop=True, inplace=True)
    return series

def plot_MA(series, MA=[7], fontsize=14, figsize=(13,6), title='Number of Trello Cards completed per day - Moving Average', tit_size=20):
    """ Create a plot of Moving Average of specified time series

    Parameters
    ----------
    series: pandas data series
        index is of date format, values ints or floats
    MA: list of ints
        which Moving Averages should be computed and plotted, e.g. [7, 30]
    fontsize: int
        fontsize for axis descriptions
    figsize: tuple of two ints
        Figure size
    title: str
        Name for the chart
    tit_size: int
        fontsize for the title

    Returns
    -------
    None
        simply creates a plot

    """
    plt.rcParams.update({'font.size': fontsize})
    fig = plt.figure(figsize=figsize)
    for item in MA:
        plt.plot(series.rolling(item).mean(), label=f'MA({item})')
    plt.grid()
    plt.legend()
    plt.title(title, fontsize=tit_size);
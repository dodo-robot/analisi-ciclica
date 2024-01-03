import pandas as pd
from calcolo_cicli import CicliAnalisiDinamica
import plotly.offline as py
import plotly.graph_objs as go

from calcolo_cicli_inverso import CicliAnalisiDinamicaInversa

# Assuming your JSON file is named "data.json"
with open('BTC_USDT_USDT-15m-futures.json') as f:
    data = pd.read_json(f, orient="records")

# Convert the array of arrays into a DataFrame
dataframe = pd.DataFrame(data=data)
dataframe.columns=['Date','Open','High','Low','Close','Volume']
#df = pd.DataFrame(data)
dataframe = dataframe.tail(600);
dataframe.reset_index(inplace=True)
dataframe['Date'] = pd.to_datetime(dataframe['Date'], unit="ms")

print(dataframe)
regole_tabella_45min = [ (-3, "giornaliero", [24, 32, 44]),
    (-4, "infragiornaliero", [12, 16, 22]),
    (-5, "metagiornata", [6, 8, 11]),
    (-6, "inframetagiornata", [3, 4, 5])
]

analisi_giornaliera = CicliAnalisiDinamica(dataframe, regole_tabella_45min[0])
ciclo4 = analisi_giornaliera.trova_cicli()
dataframe["daily"] = ciclo4


analisi_giornaliera_inversa = CicliAnalisiDinamicaInversa(dataframe, regole_tabella_45min[0])
ciclo4i = analisi_giornaliera_inversa.trova_cicli()
dataframe["daily_i"] = ciclo4i


data = [go.Candlestick(x=dataframe.Date,
                       open=dataframe.Open,
                       high=dataframe.High,
                       low=dataframe.Low,
                       close=dataframe.Close)]

layout = go.Layout(title='Bitcoin Candlestick with Range Slider',
                   xaxis={'rangeslider':{'visible':True}})

fig = go.Figure(data=data,layout=layout)
filtered_df = dataframe[dataframe['daily']==True]

print(filtered_df)

fig.add_trace(
    go.Scatter(mode = "markers",
        x=filtered_df.Date,
        y=filtered_df.Low - 100,
        name="T-3"
    ))

filtered_df_i = dataframe[dataframe['daily_i']==True]
print(filtered_df_i)
fig.add_trace(
    go.Scatter(mode = "markers",
        x=filtered_df_i.Date,
        y=filtered_df_i.High + 100,
        name="T-3i"
    ))

fig.show()




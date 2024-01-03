import pandas as pd
from calcolo_cicli import CicliAnalisiDinamica
import plotly.offline as py
import plotly.graph_objs as go

from calcolo_cicli_inverso import CicliAnalisiDinamicaInversa

dataframe = pd.read_csv("BTC-USD.csv")

regole_tabella_day = [
    (7, "quadriennale", [768, 1024, 1344]),
    (6, "biennale", [384, 512, 672]),
    (5, "annuale", [192, 256, 336]),
    (4, "semestrale", [96, 128, 168]),
    (3, "trimestrale", [48, 64, 84]),
    (2, "mensile", [24, 32, 43]),
    (1, "bisettimanale", [12, 16, 21]),
    (0, "settimanale", [6, 8, 11]),
    (-1, "infrasettimanale", [3, 4, 5])
]

regole_tabella_45min = [ (-3, "giornaliero", [24, 32, 44]),
    (-4, "infragiornaliero", [12, 16, 22]),
    (-5, "metagiornata", [6, 8, 11]),
    (-6, "inframetagiornata", [3, 4, 5])
]

analisi_quadriennale = CicliAnalisiDinamica(dataframe, regole_tabella_day[0])
ciclo4 = analisi_quadriennale.trova_cicli()
dataframe["quadriennale"] = ciclo4


analisi_quadriennale_inversa = CicliAnalisiDinamicaInversa(dataframe, regole_tabella_day[0])
ciclo4i = analisi_quadriennale_inversa.trova_cicli()
dataframe["quadriennale_i"] = ciclo4i


analisi_annuale = CicliAnalisiDinamica(dataframe, regole_tabella_day[2])
ciclo1 = analisi_annuale.trova_cicli()
dataframe["annuale"] = ciclo1


analisi_annuale_inversa = CicliAnalisiDinamicaInversa(dataframe, regole_tabella_day[2])
ciclo1i = analisi_annuale_inversa.trova_cicli()
dataframe["annuale_i"] = ciclo1i


data = [go.Candlestick(x=dataframe.Date,
                       open=dataframe.Open,
                       high=dataframe.High,
                       low=dataframe.Low,
                       close=dataframe.Close)]

layout = go.Layout(title='Bitcoin Candlestick with Range Slider',
                   xaxis={'rangeslider':{'visible':True}})

fig = go.Figure(data=data,layout=layout)
filtered_df = dataframe[dataframe['quadriennale']==True]

print(filtered_df)

fig.add_trace(
    go.Scatter(mode = "markers",
        x=filtered_df.Date,
        y=filtered_df.Low - 100,
        name="T+7"
    ))

filtered_df_i = dataframe[dataframe['quadriennale_i']==True]
print(filtered_df_i)
fig.add_trace(
    go.Scatter(mode = "markers",
        x=filtered_df_i.Date,
        y=filtered_df_i.High + 100,
        name="T+7i"
    ))

filtered_df1 = dataframe[dataframe['annuale']==True]

print(filtered_df1)

fig.add_trace(
    go.Scatter(mode = "markers",
        x=filtered_df1.Date,
        y=filtered_df1.Low - 2000,
        name="T+5"
    ))

filtered_df1_i = dataframe[dataframe['annuale_i']==True]
print(filtered_df1_i)
fig.add_trace(
    go.Scatter(mode = "markers",
        x=filtered_df1_i.Date,
        y=filtered_df1_i.High + 2000,
        name="T+5i"
    ))

fig.show()

#py.iplot(fig, filename='bitcoin_candlestick')



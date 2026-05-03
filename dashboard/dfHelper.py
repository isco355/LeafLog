import pandas as pd
import numpy as np

def tableToHeatMap(df,property):
    df['ts'] = pd.to_datetime(df['ts'])

    df['week_start'] = df['ts'] - pd.to_timedelta(df['ts'].dt.weekday, unit='d')
    df['week_start'] = df['week_start'].dt.date 

    df['day'] = df['ts'].dt.day_name()

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day'] = pd.Categorical(df['day'], categories=day_order, ordered=True)


    heatmap_data = df.pivot_table(
        index='week_start',
        columns='day',
        values=property,
        aggfunc='mean'
    )

    heatmap_data = heatmap_data.reindex(columns=day_order)

    heatmap_json = heatmap_data.fillna(0).round(2).to_dict("split")
    heatmap_json['range']={"min_val":0,"max_val":100}
    # print(heatmap_json,flush=True)
    heatmap_json['attribute']=property

    return heatmap_json


def tableToSeries(df):
    value_cols = df.select_dtypes(include="number").columns.drop('id')
    series = [
    {
        "name": col,
        "data": [
            [
                int(ts.timestamp() * 1000),
                val
            ]
            for ts, val in zip(df["ts"], df[col])
        ]
    }
    for col in value_cols]

    return series

def aggPerDevice(df):
    df= df.drop(columns=['id'])
    result = df.select_dtypes(include='number').agg([ "mean", "max", "min"]).round(2)
    return result.to_dict()


def correctionMatrix(df):
    df=df.drop(columns=['id','battery'])
    corr_matrix = df.corr(numeric_only=True)

    upper_indices = np.triu_indices_from(corr_matrix, k=1)

    corr_matrix.values[upper_indices] = 0

    corr_json=np.round(corr_matrix,decimals=2).to_dict(orient="split")
    corr_json['range']={"min_val":-1,"max_val":1}
    corr_json['attribute']="correlation"

    return corr_json


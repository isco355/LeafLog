import pandas as pd
import numpy as np

def getRange(metric):
    match metric:
        case "soil_moisture" | "humidity" | "battery":
            return {"min_val": 0, "max_val": 100}
        case "temperature":
            return {"min_val": -40, "max_val": 85}
        case "linkquality":
            return {"min_val": 0, "max_val": 255}
        case _:
            return {"min_val": None, "max_val": None}

def propertiesHeatMaps(df):
    columns=list(df.select_dtypes(include='number').drop(columns=['id']).columns)

    heatmaps_list= []
    for column_name in columns:
        heatmap = tableToHeatMap(df,column_name)
        heatmaps_list.append(heatmap)
    return heatmaps_list

def tableToHeatMap(df,property):
    df['ts'] = pd.to_datetime(df['ts'])

    df['week_start'] = df['ts'] - pd.to_timedelta(df['ts'].dt.weekday, unit='d')
    df['week_start'] = df['week_start'].dt.date 

    df['day'] = df['ts'].dt.day_name()

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day'] = pd.Categorical(df['day'], categories=day_order, ordered=True)


    df[property] =df[property].ewm(span=10, adjust=True).mean().round(2)

    heatmap_data = df.pivot_table(
        index='week_start',
        columns='day',
        values=property,
        aggfunc='mean'
    )

    heatmap_data = heatmap_data.reindex(columns=day_order)

    heatmap_json = heatmap_data.fillna(0).round(2).to_dict("split")
    range_values = getRange(property)
    heatmap_json['range']=range_values
    heatmap_json['attribute']=property

    return heatmap_json


def tableToSeries(df):
    df=df.set_index('ts')
    df=df.select_dtypes(include='number')
    df=df.drop(columns="id")
    df = df.resample('12H').mean()


    df =df.ewm(span=10, adjust=True).mean().round(2)
    series=df.to_dict(orient='series')
    json_serializable = [{"name":k,"data": v.reset_index().values.tolist()} for k, v in series.items()]


    return json_serializable

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


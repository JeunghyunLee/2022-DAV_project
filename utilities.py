import pandas as pd
import json
import plotly.express as px
areas = ["전국","서울경기","강원도","경남","경북","전남","전북","충남","충북","제주"]
mapping={
    '강원도':['강원도'],
    '강원영동':['강원도'],
    '경남':['경상남도', '울산광역시', '부산광역시'],
    '경북':['경상북도', '대구광역시'],
    '서울경기':['서울특별시', '경기도', '인천특별시'],
    '전남': ['전라남도','광주광역시'],
    '전북': ['전라북도'],
    '제주': ['제주특별자치도'],
    '충남': ['충청남도', '세종특별자치시', '대전광역시'],
    '충북':['충청북도']
}
years = list(range(1974,2023,1))

def to_map_df(df,idcol='location',datacol=['data']):
    res = pd.DataFrame(columns = [idcol]+datacol)
    for i in range(len(df)):
        temp = df[[idcol]+datacol].iloc[i] 
        key=temp[0]
        values=list(temp[1:])
        if key in mapping:
            for item in mapping[key]:
                res.loc[len(res)] = [item]+values
    return res

def loadGeo(fn='korea_sido.json'):
    geojson = json.load(open(fn,encoding='utf-8'))
    for x in geojson['features']:
        id = x['properties']['CTP_KOR_NM']
        x['id'] = id
    return geojson


def getmap(data,col='avg',loc='location',rng=(9,20)):
    geojson=loadGeo()
    fig=px.choropleth_mapbox(data,
        geojson=geojson,
        locations=loc,
        color = col,
        mapbox_style='carto-positron',
        color_continuous_scale=[(0, "blue"), (1, "red")],
        range_color=rng,
        center = {'lat':35.757981,'lon':127.661132},
        zoom=5.5,
        labels='data',
    )
    fig.update_layout(margin={"r":0,"l":0,"t":0,"b":0})
    return fig

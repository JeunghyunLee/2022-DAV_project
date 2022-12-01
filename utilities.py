import pandas as pd

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


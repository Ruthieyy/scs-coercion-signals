import requests, pandas as pd
URL="https://services9.arcgis.com/weJ1QsnbMYJlCHdG/arcgis/rest/services/Daily_Chokepoints_Data/FeatureServer/0/query"
ids=['chokepoint5','chokepoint11','chokepoint14','chokepoint25','chokepoint27','chokepoint19','chokepoint15','chokepoint20']
where=" OR ".join(f"portid='{i}'" for i in ids)
rows=[];off=0
while True:
    r=requests.get(URL,params=dict(where=where,outFields="*",returnGeometry="false",f="json",resultOffset=off,resultRecordCount=2000),timeout=60).json()
    feats=r.get('features',[]); rows+= [f['attributes'] for f in feats]
    if len(feats)==0 or not r.get('exceededTransferLimit') and len(feats)<2000: break
    off+=len(feats)
df=pd.DataFrame(rows); df['date']=pd.to_datetime(df['date'],unit='ms')
df.to_csv('data/raw/portwatch_scs_chokepoints.csv',index=False)
print(df.shape, list(df.columns))
print(df.groupby('portname').agg(start=('date','min'),end=('date','max'),n=('date','size'),mean_total=('n_total','mean')).round(1))

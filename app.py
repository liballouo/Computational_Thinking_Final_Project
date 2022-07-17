from flask import Flask,render_template
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import json
from numpy.lib.npyio import save
from requests import request

app=Flask(__name__) # __name__代表目前執行的模組

#建立地圖，中間點為自己設定的位置，預設位置為成功大學
def map1(lat='22.996783',lon = '120.219639',score = 16,map_type = 'cartodbpositron'):
    ##製作map
    map = folium.Map(location=[lat,lon],zoom_start=score,tiles=map_type)
    folium.Marker(
        [lat,lon],
        popup= '現在位置',
        tooltip='tooltip', 
        icon=folium.Icon(color='red')
    ).add_to(map)
    return(map)
#距離公式
from math import radians, cos, sin, asin, sqrt
 
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    # haversine公式
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # 地球平均半径，单位为公里
    return c * r 

#建立熱力圖
def heat_map(map,lat=0,lon=0,type=0,distance = 1,url = 'ans.csv',color="#555",fill_color='#FFE082'):
    import csv
    type = int(type)
    distance = int(distance)
    #print('==============================================')
    with open(url,'r',encoding='utf-8-sig') as f:
        
        datas =  csv.reader(f)
        data = list(datas)
        del data[0]
    dictionary ={}
    for i in data:
        if i[type] == '0.0':
            continue
        else: 
            try:
                dictionary[i[1]].append(float(i[type]))
            except:
                try:
                    dictionary[i[1]] = [float(i[type])]
                except:
                    continue 
    numbers = 0
    for i in range(1,len(data)):
        try:
            if (haversine(float(lon),float(lat),float(data[i][3]),float(data[i][2]))<=distance):
                try:
                    #append_data = [data[i][2],data[i][3],len(dictionary[data[i][1]])]
                    #total_data.append(append_data)
                    folium.Circle(
                        radius=25,
                        location=[data[i][2],data[i][3]],
                        popup= '['+str(len(dictionary[data[i][1]]))+']['+str(sum(dictionary[data[i][1]])).replace('.0','')+'] '+data[i][1],
                        tooltip='tooltip',
                        color=color,
                        weight=1,
                        fill_color=fill_color,
                        fill_opacity=1,
                    ).add_to(map)
                    numbers+=1
                except:
                    continue    
        except:
            continue

    if numbers == 0:
        return('此範圍內無拖吊紀錄')    
    else:  
        return(map)

#在地圖上建立圓點，預設網址為機車路邊停車格，顏色預設為粉紅色
def add_point(map,url ='https://citypark.tainan.gov.tw/App/parking.ashx?verCode=5177E3481D&type=4&ftype=1&exportTo=2',type1='一般機車',lon=0,lat=0,distance=1,color="#555",fill_color="#FFE082"):
    ##抓取網路資料並放入data裡
    distance = int(distance)
    if type(url) != list:
        url = [url]
    if type(color) != list:
        color = [color]
    if type(fill_color) != list:
        fill_color = [fill_color]
    numbers = 0    
    for xx,x in enumerate(url):
        data = json.loads(request('GET', x).text)
        for i in range(0,len(data)):
            if(data[i]['經緯度'] == None):
                continue
            if(data[i][type1] == 0):
                continue
            ang = data[i]['經緯度'].split('，')
            if (haversine(float(lon),float(lat),float(ang[1]),float(ang[0]))<=distance):
                folium.Circle(
                    radius=25,
                    location=[ang[0],ang[1]],
                    popup= data[i]['停車場型態']+'['+str(data[i][type1])+']',
                    color=color[xx],
                    weight=1,
                    fill_color=fill_color[xx],
                    fill_opacity=1,
                    #icon=folium.Icon(color=color)
                ).add_to(map)
                numbers+=1
    if numbers == 0:
        return('此範圍內無登記之政府停車格')      
    else:
        return(map)

def add_point1(map,data,lon=0,lat=0,distance=1,color="#555",fill_color="#FFE082"):
    ##抓取網路資料並放入data裡
    numbers = 0
    for i in data:
        distance = int(distance)
        if (haversine(float(lon),float(lat),float(i[1]),float(i[0]))<=distance):
            folium.Circle(
                radius=25,
                location=[i[0],i[1]],
                popup= i[2],
                color=color,
                weight=1,
                fill_color=fill_color,
                fill_opacity=1,
                #icon=folium.Icon(color=color)
            ).add_to(map)
            numbers += 1    
    if numbers == 0:
        return('此範圍內無您所尋找之標的物')      
    else:
        return(map)
#網頁訊息
def gogoro():
    import urllib.request as req
    url = "https://webapi.gogoro.com/api/vm/list"
    request = req.Request(url, headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    #print(data)
    data = json.loads(data)
    tainan = data[2565:]
    data = []
    for i in tainan:
        x = i['Latitude']
        y = i['Longitude']
        z = i['Address'][:-19]
        a = z.split('},')[1]
        address = a[10:]
        data.append([x,y,address])
    return(data)

def get_information(path):
    import json
    with open(path,'r',encoding='utf-8') as f:
        datas = json.load(f)
        data = []
        for key,value in datas.items():
            value.reverse()
            value.append(key)
            data.append(value)
    return(data)
#基礎網頁(點進去看到的第一個東西)
@app.route("/") # 函式的裝飾:以函式為基礎，提供附加的功能
def home():
    m = map1()
    return(m._repr_html_())

#附加網頁，尋找附近的路邊機車格
@app.route('/<num1>&<num2>/<num3>&<num4>&<num5>&<num6>/<num7>/<num8>', methods=['GET'])
def index(num1,num2,num3,num4,num5,num6,num7,num8):
    # num1:緯度 num2:經度 num3:路邊停車 num4:公有要錢 num5:公有免錢 num6:私有要錢 
    m = map1(num1,num2)
    url = []
    if(num3 == '1'):
        url.append('https://citypark.tainan.gov.tw/App/parking.ashx?verCode=5177E3481D&type=4&ftype=1&exportTo=2')
    if(num4 == '1'):
        url.append('https://citypark.tainan.gov.tw/App/parking.ashx?verCode=5177E3481D&type=2&ftype=1&exportTo=2')
    if(num5 == '1'):
        url.append('https://citypark.tainan.gov.tw/App/parking.ashx?verCode=5177E3481D&type=1&ftype=1&exportTo=2')
    if(num6 == '1'):
        url.append('https://citypark.tainan.gov.tw/App/parking.ashx?verCode=5177E3481D&type=3&ftype=1&exportTo=2')
    co = ["#FFE082",'pink','yellow','#3186cc']
    co1 = ["#555","#555","#555","#555"]
    m = add_point(m,url,num7,num2,num1,num8,co1,co)
    if(type(m) == str):
        return(m)
    else:
        return(m._repr_html_()) 

#找拖吊
@app.route('/<num1>&<num2>/botang/<num7>/<num8>', methods=['GET'])
def index1(num1,num2,num7,num8):
    m = map1(num1,num2)
    m = heat_map(m,num1,num2,num7,num8)
    if(type(m) == str):
        return(m)
    else:
        return(m._repr_html_())  
#找gogoro
@app.route('/<num1>&<num2>/gogoro/<num8>', methods=['GET'])
def gogoro_battery(num1,num2,num8):
    m = map1(num1,num2)
    data = gogoro()
    m = add_point1(m,data,num2,num1,num8)
    if(type(m) == str):
        return(m)
    else:
        return(m._repr_html_())

@app.route('/<num1>&<num2>/gas_station/<num8>', methods=['GET']) 
def find_gas_station(num1,num2,num8):
    m = map1(num1,num2)
    data = get_information('gas_station.json')
    m = add_point1(m,data,num2,num1,num8)
    if(type(m) == str):
        return(m)
    else:
        return(m._repr_html_())

@app.route('/<num1>&<num2>/stolen/<num8>', methods=['GET']) 
def stolen(num1,num2,num8):
    m = map1(num1,num2)
    data = get_information('steal.json')
    m = add_point1(m,data,num2,num1,num8)
    if(type(m) == str):
        return(m)
    else:
        return(m._repr_html_())

if __name__ == "__main__":# 如果以主程式執行
    app.run(debug=True) # 立刻啟用伺服器
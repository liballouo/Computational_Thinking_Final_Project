# 使用地圖網頁

## 首先須執行app.py
以下為使用方法介紹，若有問題請mail我(xt21109142@gmail.com)，或在fb私訊我(廖柏棠)
## 執行後在terminal會出現網址，開啟網址後即可出現地圖。

### 查詢停車資訊功能
原網址後需輸入 /<緯度>&<經度>/1&1&1&1/<交通工具類型>/<查詢方圓半徑>

- 緯度:欲查詢位置的緯度
- 精度:欲查詢位置的經度
- 交通工具類型:
  包含
  - 一般大型車
  - 一般小型車
  - 身障者小型車
  - 婦幼者小型車
  - 綠能小型車
  - 一般機車
  - 身障者機車
- 輸入半徑(單位公里)即可顯示半徑範圍內的停車位

Example: 

http://127.0.0.1:5000/23&120.219639/1&1&1&1/一般機車/1 
其意旨為查看緯度23度，經度120.219639處半徑一公里的一般機車停車位
- http://127.0.0.1:5000 為terminal顯示之網址。
- /23&120.219639 為欲查詢位置的緯度與經度
- /1&1&1&1 略過(若有興趣可自行在app.py的註解中察看)
- /一般機車 為交通工具類型
- 網址最後的1 為半徑一公里內

### 查詢拖吊熱點功能
原網址後需輸入 /<緯度>&<經度>/botang/<交通工具類型>/<查詢方圓半徑>
- 緯度:欲查詢位置的緯度
- 精度:欲查詢位置的經度
- 交通工具類型:
  包含
  - 一般機車  (輸入0)
  - 一般汽車 (輸入4)
  - 大型汽車 (輸入5)
  - 重型機車 (輸入6)
- 輸入半徑(單位公里)即可顯示半徑範圍內的拖吊位置與頻率

Example:

http://127.0.0.1:5000/23&120.219639/botang/4/1

其意旨為查看緯度23度，經度120.219639處半徑一公里的一般汽車拖吊頻率

### 查詢其他功能
原網址後需輸入 /<緯度>&<經度>/<功能>/<查詢方圓半徑>
- 緯度:欲查詢位置的緯度
- 精度:欲查詢位置的經度
- 交通工具類型:
  包含
  - 查詢附近加油站  (輸入 gas_station)
  - 查詢附近gogoro充電站 (輸入 gogoro)
  - 查詢附近的機車竊盜事件 (輸入 stolen)
- 輸入半徑(單位公里)即可顯示半徑範圍內的停車位

Example:

http://127.0.0.1:5000/23&120.219639/gas_station/2
其意旨為查看緯度23度，經度120.219639處半徑兩公里的加油站 

http://127.0.0.1:5000/23&120.219639/gogoro/1
其意旨為查看緯度23度，經度120.219639處半徑一公里的gogoro充電站 

http://127.0.0.1:5000/23&120.219639/stolen/1
其意旨為查看緯度23度，經度120.219639處半徑一公里的機車竊盜事件
#获取成都的公交站点的分布情况。并在地图上展示出来。python3

bus_info.csv有成都所有公交站的名字

get_bus_station_info.py通过百度地图webapi，获取公交站的坐标，保存为bus_station_info2.csv(因为网站限制一天只能2000次，所以分了两次取下来)

generate_bus_coordinate.py 把信息整理成echarts需要的格式，保存为bus_station_location.json

用npx webpack --watch src/map_pack.js dist/bundle.js来生成js。index.html来显示页面

用notejs的httpserver来查看最后的结果



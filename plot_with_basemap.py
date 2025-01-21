from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

connection = sqlite3.connect("data/minard.db")
city_df = pd.read_sql("""SELECT * FROM cities;""", con=connection)
temperature_df = pd.read_sql("""SELECT * FROM temperatures;""", con=connection)
troop_df = pd.read_sql("""SELECT * FROM troops;""", con=connection)
connection.close()

loncs = city_df["lonc"].values
latcs = city_df["latc"].values
city_names = city_df["city"].values
rows = troop_df.shape[0]
lonps = troop_df["lonp"].values
latps = troop_df["latp"].values
survivals = troop_df["surviv"].values
directions = troop_df["direc"].values
#設定畫布尺寸和三張圖比例
fig, axes = plt.subplots(nrows=2, figsize=(25,12), gridspec_kw={"height_ratios": [4, 1]})
#城市圖
m = Basemap(projection="lcc", resolution="i", width=1000000, height=400000,
            lon_0=31, lat_0=55, ax=axes[0])
m.drawcountries()
m.drawrivers() #地圖上出現河流
m.drawparallels(range(54, 58),labels=[True, False, False, False]) #只要圖左邊有標示
m.drawmeridians(range(23, 56, 2),labels=[False, False, False, True]) #只要圖下方有標示
x, y = m(loncs, latcs)
for xi, yi, city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name, xy=(xi, yi), fontsize=14, zorder=2)
#軍隊路線圖
x, y = m(lonps, latps)
for i in range(rows - 1):
    if directions[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"
    start_stop_lons = (x[i], x[i + 1])#每個線段是分開畫的
    start_stop_lats = (y[i], y[i + 1])
    line_width = survivals[i]#線條寬度是軍隊人數
    m.plot(start_stop_lons, start_stop_lats, linewidth=line_width/10000, color=line_color, zorder=1)
#氣溫圖
temp_celsius = (temperature_df["temp"] * 5/4).astype(int)#改攝式溫度
annotations = temp_celsius.astype(str).str.cat(temperature_df["full_date"], sep="°C ")#在dataFrame中串接字符
lonts = temperature_df["lont"].values
axes[1].plot(lonts, temp_celsius, linestyle="dashed", color="black")
for lont, temp_c, annotation in zip(lonts, temp_celsius, annotations):
    axes[1].annotate(annotation, xy=(lont - 0.3, temp_c - 7), fontsize=10)
axes[1].set_ylim(-50, 10)
#隱藏第二個子圖上下左右的四個邊框
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].grid(True, which="major", axis="both")#增加網格線
#隱藏 x 軸與 y 軸刻度標籤
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
axes[0].set_title("Napoleon's disastrous Russian campaign of 1812", loc="left", fontsize=30)
plt.tight_layout()
fig.savefig("minard_clone.png")
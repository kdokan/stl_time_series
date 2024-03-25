
#%%
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot
from statsmodels.tsa.seasonal import STL



#%%
path_data = "../data/data.csv"


# データ読み込み
data = pd.read_csv(
    path_data
    , skiprows=1)

# カラム名設定
data = data.rename(
    columns = {
        "週":"ds",
        "バファリン: (日本)":"search_volume_for_bufferin"
    }
)

# 日付型に変換
data["ds"] = pd.to_datetime(data["ds"])

# データの中身確認
plt.plot(data["ds"],data["search_volume_for_bufferin"])



# %%
stl = STL(data["search_volume_for_bufferin"], period = 53, robust=True)
stl_series = stl.fit()
stl_series.plot()
plt.show()

# %%
data_stl = {
    "ds": data["ds"],
    "search_volume_for_bufferin": stl_series.observed,
    "trend": stl_series.trend,
    "seasonal": stl_series.seasonal,
    "resid": stl_series.resid
}

data_stl = pd.DataFrame(data_stl)
data_stl


# %%

# PlotlyのFigureオブジェクトを作成
fig = go.Figure()

# 折れ線グラフを追加
fig.add_trace(go.Scatter(x=data_stl['ds'], y=data_stl['search_volume_for_bufferin'], mode='lines', name='Search Volume for Bufferin'))
fig.add_trace(go.Scatter(x=data_stl['ds'], y=data_stl['trend'], mode='lines', name='Trend'))
fig.add_trace(go.Scatter(x=data_stl['ds'], y=data_stl['seasonal'], mode='lines', name='Seasonal'))
fig.add_trace(go.Scatter(x=data_stl['ds'], y=data_stl['resid'], mode='lines', name='Resid'))

# レイアウトの設定
fig.update_layout(title='Search Volume for Bufferin', xaxis_title='Date', yaxis_title='Value')

# HTMLファイルにグラフを保存してブラウザで開く
plot(fig, filename='bufferin_search_volume.html')


# %%

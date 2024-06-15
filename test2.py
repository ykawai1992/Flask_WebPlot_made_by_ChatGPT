import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot_hourly/<filename>')
def plot_hourly(filename):
    # フォルダパス
    hourly_folder = 'D:/2_共同研究/常陸放送設備株式会社/R060514_Flask経由でWebへ表示_CHATGPT/plot_hourly'
    filepath = os.path.join(hourly_folder, filename)
    
    if not os.path.exists(filepath):
        return f"File {filepath} does not exist.", 404
    
    # CSVファイルをPandas DataFrameとして読み込む
    df = pd.read_csv(filepath, header=None, names=['Timestamp', 'Power'])
    
    # Timestamp列を日時型に変換
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y/%m/%d %H:%M')
    except ValueError as e:
        return f"ValueError: {e}. Ensure the Timestamp format matches the data.", 500
    
    # グラフを描画
    plt.figure(figsize=(10, 6))
    plt.plot(df['Timestamp'], df['Power'], marker='o', linestyle='-')
    plt.title('Hourly Power Data')
    plt.xlabel('Timestamp')
    plt.ylabel('Power')
    plt.grid(True)
    
    # グラフを一時ファイルとして保存
    plot_filename = 'plot_hourly.png'
    plot_filepath = os.path.join(app.root_path, 'static', plot_filename)
    plt.savefig(plot_filepath)
    plt.close()
    
    return render_template('plot.html', plot_url=f'/static/{plot_filename}')

@app.route('/plot_daily/<filename>')
def plot_daily(filename):
    # フォルダパス
    daily_folder = 'D:/2_共同研究/常陸放送設備株式会社/R060514_Flask経由でWebへ表示_CHATGPT/plot_daily'
    filepath = os.path.join(daily_folder, filename)
    
    if not os.path.exists(filepath):
        return f"File {filepath} does not exist.", 404
    
    # CSVファイルをPandas DataFrameとして読み込む
    df = pd.read_csv(filepath, header=None, names=['Timestamp', 'Power'])
    
    # Timestamp列を日時型に変換
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y/%m/%d %H:%M')
    except ValueError as e:
        return f"ValueError: {e}. Ensure the Timestamp format matches the data.", 500
    
    # 日別データの集計
    df.set_index('Timestamp', inplace=True)
    daily_data = df.resample('D').sum()
    
    # グラフを描画
    plt.figure(figsize=(10, 6))
    plt.plot(daily_data.index, daily_data['Power'], marker='o', linestyle='-')
    plt.title('Daily Power Data')
    plt.xlabel('Date')
    plt.ylabel('Power')
    plt.grid(True)
    
    # グラフを一時ファイルとして保存
    plot_filename = 'plot_daily.png'
    plot_filepath = os.path.join(app.root_path, 'static', plot_filename)
    plt.savefig(plot_filepath)
    plt.close()
    
    return render_template('plot.html', plot_url=f'/static/{plot_filename}')

if __name__ == '__main__':
    app.run(debug=True)

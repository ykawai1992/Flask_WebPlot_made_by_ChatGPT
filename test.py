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
    # 修正したフォルダパス
    hourly_folder = 'D:/2_共同研究/常陸放送設備株式会社/R060514_Flask経由でWebへ表示_ChatGPT/plot_hourly'
    filepath = os.path.join(hourly_folder, filename)
    
    if not os.path.exists(filepath):
        return f"File {filepath} does not exist.", 404
    
    # CSVファイルをPandas DataFrameとして読み込む
    df = pd.read_csv(filepath, header=None, names=['Timestamp', 'Power'])
    
    # デバッグ: 読み込んだデータフレームの最初の数行を表示
    print("CSVファイルの最初の数行:")
    print(df.head())
    
    # 列名を確認
    print("データフレームの列名:")
    print(df.columns)
    
    # Timestamp列を日時型に変換
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y/%m/%d %H:%M')
    except KeyError as e:
        return f"KeyError: {e}. Available columns: {df.columns}", 500
    
    # グラフを描画
    plt.figure(figsize=(10, 6))
    plt.plot(df['Timestamp'], df['Power'], marker='o', linestyle='-')
    plt.title('Hourly Power Data')
    plt.xlabel('Timestamp')
    plt.ylabel('Power')
    plt.grid(True)
    
    # グラフを一時ファイルとして保存
    plot_filename = 'plot.png'
    plot_filepath = os.path.join(app.root_path, 'static', plot_filename)
    plt.savefig(plot_filepath)
    plt.close()
    
    return render_template('plot.html', plot_url=f'/static/{plot_filename}')

if __name__ == '__main__':
    app.run(debug=True)

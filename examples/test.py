import shutil  # 匯入尋找系統 FFmpeg 的工具
from pathlib import Path  # 匯入處理檔案路徑的工具

import imageio_ffmpeg  # 匯入提供專案內 FFmpeg 的套件
import yt_dlp  # 匯入 yt-dlp 套件，用於下載 YouTube 影片

target_url = "https://www.youtube.com/watch?v=-RmUADCWI4A"

ydl_opts = {
    'format': 'bv*+ba/b',  # 下載最佳影像與最佳音訊，然後合併；無法分離時退回最佳格式
    'outtmpl': str(Path('video_output') / '%(title)s [%(id)s].%(ext)s'),  # 將影片輸出到 video_output
    'merge_output_format': 'mp4',  # 將影像與音訊合併成 MP4
    'quiet': True,                   # 不印出雜亂的下載進度訊息
    'noplaylist': True,              # 只解析指定影片，不解析整個播放清單
    'js_runtimes': {'node': {}},     # 使用已安裝的 Node.js 執行 YouTube JavaScript challenge
    'remote_components': ['ejs:github'],  # 下載 yt-dlp 官方 EJS challenge solver
    'ffmpeg_location': str(shutil.which('ffmpeg') or imageio_ffmpeg.get_ffmpeg_exe()),  # 指定 FFmpeg 執行檔路徑
}

print("正在解析 YouTube 影片串流，請稍候...")

ydl = yt_dlp.YoutubeDL(ydl_opts) 
try:
    # 提取影片資訊
    info_dict = ydl.extract_info(target_url, download= True)
    print(info_dict)  # 印出影片資訊找到 url 的位置
    # 取得真正的影片串流網址 (Stream URL)
    stream_url = info_dict.get('url', None)
    if not stream_url:
        print("無法取得影片串流網址。")
        exit()    
except Exception as e:
    print(f"解析失敗，請檢查網址或網路連線。錯誤訊息: {e}")
    exit()


print(f"成功取得影片串流網址：{stream_url}")
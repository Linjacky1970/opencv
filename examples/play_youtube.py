import cv2
import yt_dlp

# 1. 先取得影片串流							
# 設定 yt-dlp 參數，指定只抓取包含有影像的格式
target_url = "https://www.youtube.com/watch?v=-IHzsbRSabE"
ydl_opts = {
    'format': 'bestvideo[ext=mp4]/bestvideo/best',  # 優先選擇包含影像的最佳 MP4 畫質
    'quiet': True,                   # 不印出雜亂的下載進度訊息
    'noplaylist': True,              # 只解析指定影片，不解析整個播放清單
    'js_runtimes': {'node': {}},     # 使用已安裝的 Node.js 執行 YouTube JavaScript challenge
    'remote_components': ['ejs:github'],  # 下載 yt-dlp 官方 EJS challenge solver
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

# 2. 將串流網址傳給 OpenCV 的 VideoCapture
cap = cv2.VideoCapture(stream_url)

print("成功開啟影片！按下 'Esc' 鍵可隨時退出。")

# 3. 逐幀讀取與處理影像
while cap.isOpened():
    ret, frame = cap.read()
    
    # 如果沒有讀取到幀，代表影片結束或串流中斷
    if not ret:
        print("影片播放結束或訊號中斷。")
        break

    # 即時將影像調整大小，並轉為灰階（模擬 AI 預處理）
    resized_frame = cv2.resize(frame, (640, 360))
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # 顯示影像視窗
    cv2.imshow('YouTube Original (Resized)', resized_frame)
    cv2.imshow('YouTube Gray Effect', gray_frame)

    # 控制播放速度 (約每幀等待 33 毫秒)，並偵測是否按下 'ESC' 鍵退出
    if cv2.waitKey(33) & 0xFF == 27:
        break

# 4. 釋放資源
cap.release()
cv2.destroyAllWindows()
print("播放結束。")
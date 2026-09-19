from pathlib import Path  # 匯入處理檔案路徑的工具
import numpy as np  # 匯入數值運算套件
import cv2  # 匯入 OpenCV 套件

image_path = Path(__file__).resolve().parent / "people01.jpg"  # 以程式所在資料夾為基準設定圖片路徑
image = cv2.imread(str(image_path))  # 讀取 people01.jpg 圖片

if image is None:  # 檢查圖片是否讀取成功
    raise FileNotFoundError(f"找不到或無法讀取圖片：{image_path}")  # 讀取失敗時顯示錯誤訊息

resized_image = cv2.resize(image, (800, 600))  # 將圖片縮放為寬 800、高 600 像素
gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)  # 將 BGR 三通道依 Gray=0.114B+0.587G+0.299R 轉換成單通道灰階影像
gray_bgr_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)  # 將灰階單通道轉回三通道，讓它能與彩色圖水平拼接
combined_image = cv2.vconcat([resized_image, gray_bgr_image])  # 將原圖與灰階圖由上到下垂直堆疊
cv2.imshow("people01 - Original and Gray", combined_image)  # 建立視窗並顯示垂直堆疊後的圖片
npStack = np.hstack((resized_image, gray_bgr_image)) 
vstack=np.vstack((npStack, npStack))  # 將原圖與灰階圖由左到右水平堆疊
cv2.imshow('np stack', vstack)  # 建立視窗並顯示水平堆疊後的圖片
 # 將原圖與灰階圖由左到右水平堆疊

print(f"原圖 shape：{resized_image.shape}")  # 顯示原圖的高度、寬度與三個色彩通道
print(f"灰階圖 shape：{gray_image.shape}")  # 顯示灰階圖的高度與寬度
print(f"堆疊圖 shape：{combined_image.shape}")  # 顯示垂直堆疊後的總高度、寬度與三個色彩通道
cv2.waitKey(0)  # 等待使用者按下任意按鍵
cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗

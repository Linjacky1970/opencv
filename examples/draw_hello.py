import cv2  # 匯入 OpenCV 套件
import numpy as np  # 匯入 NumPy 套件，用來建立畫布

canvas = np.zeros((512, 512, 3), dtype=np.uint8)  # 建立 512x512 的黑色三通道畫布
canvas[:] = (0, 255, 0)  # 將畫布填滿綠色，OpenCV 使用 BGR 順序

cv2.putText(  # 在畫布上繪製文字
    canvas,  # 指定要繪製文字的畫布
    "Hello",  # 指定要顯示的文字內容
    (100, 100),  # 指定文字左下角基準點座標
    cv2.FONT_HERSHEY_SIMPLEX,  # 指定文字字體
    3,  # 指定字體大小倍率
    (0, 0, 255),  # 指定文字顏色為紅色，OpenCV 使用 BGR 順序
    5,  # 指定文字線寬為 5
    cv2.LINE_AA,  # 啟用抗鋸齒效果
)  # 完成文字繪製

cv2.imshow("Blue Canvas", canvas)  # 建立視窗並顯示藍色畫布與紅色文字
cv2.waitKey(0)  # 等待使用者按下任意按鍵
cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗

from datetime import datetime  # 匯入取得目前日期與時間的工具
from pathlib import Path  # 匯入處理檔案路徑的工具
import time  # 匯入取得系統時間的工具

import cv2  # 匯入 OpenCV 套件
import numpy as np  # 匯入 NumPy 影像陣列處理工具


def save_frame(frame) -> bool:  # 定義儲存目前畫面的函式
    capture_directory = Path("captures")  # 設定截圖儲存資料夾
    capture_directory.mkdir(parents=True, exist_ok=True)  # 確保截圖資料夾存在
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # 產生包含微秒的時間戳
    output_path = capture_directory / f"capture_{timestamp}.jpg"  # 建立截圖檔案路徑
    is_saved = cv2.imwrite(str(output_path), frame)  # 將目前畫面儲存成 JPG 檔案
    if is_saved:  # 檢查截圖是否成功儲存
        print(f"截圖已儲存：{output_path}")  # 顯示截圖儲存位置
    return is_saved  # 回傳截圖是否成功儲存


def main() -> None:  # 定義程式主入口函式
    cap = cv2.VideoCapture("videos/people02.mp4")  # 開啟指定的影片檔案
    if not cap.isOpened():  # 檢查影片是否成功開啟
        raise RuntimeError("無法開啟影片：videos/people02.mp4")  # 開啟失敗時顯示錯誤訊息

    display_mode = 1  # 設定初始顯示模式為原始畫面
    mode_names = {1: "模式1：原始畫面", 2: "模式2：灰階", 3: "模式3：Canny 邊緣"}  # 設定顯示模式名稱
    previous_time = time.time()  # 記錄前一幀的系統時間
    is_paused = False  # 設定影片初始為播放狀態
    processed_frame_count = 0  # 記錄實際處理的影片幀數
    processing_time = 0.0  # 累計影片幀的處理時間
    screenshot_count = 0  # 記錄成功儲存的截圖數量
    video_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # 取得影片總幀數
    video_fps = cap.get(cv2.CAP_PROP_FPS)  # 取得影片原始 FPS
    video_duration = video_frame_count / video_fps if video_fps > 0 else 0.0  # 計算影片總時長秒數

    try:  # 使用 try 確保影片資源最後會被釋放
        while True:  # 持續讀取並顯示影片畫面
            if not is_paused:  # 判斷目前是否為播放狀態
                success, frame = cap.read()  # 從影片讀取下一格畫面
                if not success:  # 檢查是否已到影片結尾或讀取失敗
                    break  # 讀取失敗時結束主迴圈

                current_time = time.time()  # 取得目前幀的系統時間
                frame_interval = current_time - previous_time  # 計算目前幀與前一幀的時間間隔
                fps = 1 / frame_interval if frame_interval > 0 else 0.0  # 根據兩幀間隔計算即時 FPS
                previous_time = current_time  # 更新前一幀的系統時間
                video_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # 取得目前影片時間並換算成秒
                processed_frame_count += 1  # 增加實際處理的影片幀數
                processing_time += frame_interval  # 累加目前幀的處理時間

            original_frame = frame.copy()  # 複製目前畫面供左側顯示

            if display_mode == 1:  # 判斷目前是否為原始畫面模式
                display_frame = frame  # 使用原始畫面作為顯示畫面
            elif display_mode == 2:  # 判斷目前是否為灰階模式
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 將畫面轉換成灰階
                display_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)  # 將灰階畫面轉回 BGR 以便顯示
            else:  # 目前為 Canny 邊緣偵測模式
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 將畫面轉換成灰階
                edge_frame = cv2.Canny(gray_frame, 100, 200)  # 使用 Canny 偵測畫面邊緣
                display_frame = cv2.cvtColor(edge_frame, cv2.COLOR_GRAY2BGR)  # 將邊緣畫面轉回 BGR 以便顯示

            cv2.putText(original_frame, "Original", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)  # 在左側畫面標註原始畫面
            cv2.putText(display_frame, "Processed", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)  # 在右側畫面標註處理後畫面
            cv2.putText(display_frame, mode_names[display_mode], (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)  # 在右側畫面顯示目前模式名稱
            cv2.putText(display_frame, f"Video Time: {video_timestamp:.2f} s", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)  # 在右側畫面顯示藍色影片時間戳
            cv2.putText(display_frame, f"FPS: {fps:.1f}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)  # 在右側畫面顯示藍色即時 FPS
            combined_frame = np.hstack((original_frame, display_frame))  # 將原始畫面與處理後畫面水平並排
            cv2.imshow("People Video", combined_frame)  # 在同一個視窗顯示並排畫面
            key = cv2.waitKey(10) & 0xFF  # 等待鍵盤輸入並保留按鍵的低 8 位元
            if key == 27 or key == ord("q"):  # 判斷是否按下 ESC 或 q 鍵
                break  # 離開影片播放迴圈
            if key == ord(" "):  # 判斷是否按下空白鍵
                is_paused = not is_paused  # 在暫停與播放狀態之間切換
                previous_time = time.time()  # 更新計時基準避免將暫停時間算入 FPS
            if key in (ord("1"), ord("2"), ord("3")):  # 判斷是否按下模式切換數字鍵
                display_mode = int(chr(key))  # 將按下的數字鍵設定為目前顯示模式
            if key == ord("s"):  # 判斷是否按下 s 鍵
                if save_frame(combined_frame):  # 嘗試儲存目前並排顯示的影片畫面
                    screenshot_count += 1  # 儲存成功時增加截圖數量
    finally:  # 無論如何都執行影片資源清理
        cap.release()  # 釋放影片讀取資源
        cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗

    average_processing_fps = processed_frame_count / processing_time if processing_time > 0 else 0.0  # 計算平均處理 FPS
    print(f"總播放幀數：{processed_frame_count}")  # 輸出總播放幀數
    print(f"平均處理 FPS：{average_processing_fps:.1f}")  # 輸出平均處理 FPS
    print(f"影片總時長：{video_duration:.2f} 秒")  # 輸出影片總時長
    print(f"本次共儲存幾張截圖：{screenshot_count}")  # 輸出本次儲存的截圖數量


if __name__ == "__main__":  # 確認此檔案是直接執行
    main()  # 執行程式主入口
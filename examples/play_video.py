from datetime import datetime  # 匯入取得目前日期與時間的工具
import sys  # 匯入讀取命令列參數的工具
import time  # 匯入控制重試間隔的工具

import cv2  # 匯入 OpenCV 套件


WINDOW_NAME = "OpenCV Video Player"  # 設定影片播放視窗名稱
RESIZE_SCALE = 1  # 設定影片畫面縮放為原始尺寸的 50%
DEFAULT_SOURCE = "https://tcnvr4.taichung.gov.tw/85dd7d3d"  # 設定預設 CCTV 串流網址
MAX_READ_RETRIES = 5  # 設定 cap.read() 失敗時最多重新連線次數
RETRY_DELAY_SECONDS = 2  # 設定每次重新連線前等待秒數


def open_capture(source: str) -> tuple[cv2.VideoCapture, float]:  # 定義開啟來源並取得 FPS 的函式
    capture = cv2.VideoCapture(source)  # 開啟影片檔案或 CCTV 串流

    if not capture.isOpened():  # 檢查影片是否成功開啟
        capture.release()  # 開啟失敗時釋放目前的串流資源
        raise RuntimeError(f"無法開啟影片或串流：{source}")  # 開啟失敗時顯示錯誤訊息

    video_fps = capture.get(cv2.CAP_PROP_FPS)  # 取得影片或串流提供的 FPS
    if video_fps <= 0:  # 檢查影片是否提供有效的 FPS
        video_fps = 30.0  # 若影片沒有 FPS，使用 30 FPS 作為預設值
    return capture, video_fps  # 回傳已開啟的來源與有效 FPS


def play_video(source: str) -> None:  # 定義影片播放函式
    capture, video_fps = open_capture(source)  # 開啟指定的影片檔案或 CCTV 串流

    delay = max(1, round(1000 / video_fps))  # 依影片 FPS 計算每格畫面的等待毫秒數
    is_paused = False  # 設定影片初始為播放狀態
    read_retries = 0  # 記錄連續讀取失敗次數

    try:  # 使用 try 確保影片資源最後會被釋放
        while True:  # 持續讀取與顯示影片畫面
            if not is_paused:  # 只有未暫停時才讀取下一格畫面
                success, frame = capture.read()  # 從影片讀取下一格畫面
                if not success:  # 檢查是否已讀到影片結尾或讀取失敗
                    read_retries += 1  # 增加連續讀取失敗次數
                    if read_retries > MAX_READ_RETRIES:  # 檢查是否已超過最大重試次數
                        print("連續讀取失敗，已停止播放。")  # 顯示停止播放原因
                        break  # 超過重試上限後結束播放迴圈
                    capture.release()  # 重新連線前先釋放舊的串流資源
                    print(f"讀取失敗，{RETRY_DELAY_SECONDS} 秒後第 {read_retries} 次重新連線...")  # 顯示重試進度
                    time.sleep(RETRY_DELAY_SECONDS)  # 等待串流服務恢復
                    try:  # 嘗試重新開啟影片或 CCTV 串流
                        capture, video_fps = open_capture(source)  # 重新建立串流連線並更新 FPS
                        delay = max(1, round(1000 / video_fps))  # 依重新取得的 FPS 更新等待時間
                    except RuntimeError:  # 捕捉重新連線失敗
                        continue  # 保留重試次數並進入下一輪重試
                    continue  # 重新連線成功後回到迴圈讀取影格
                read_retries = 0  # 成功讀取影格後清除連續失敗計數
                frame = cv2.resize(frame, None, fx=RESIZE_SCALE, fy=RESIZE_SCALE)  # 將目前畫面縮小為原尺寸的 0.5 倍

            status = "PAUSED" if is_paused else "PLAYING"  # 根據狀態準備顯示文字
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 取得目前系統時間並格式化
            time_text = f"Time: {current_time}"  # 建立目前時間顯示文字
            fps_text = f"FPS: {video_fps:.2f} | {status}"  # 建立目前 FPS 與播放狀態文字
            cv2.putText(  # 將目前時間繪製到畫面上
                frame,  # 指定要繪製文字的影片畫面
                time_text,  # 指定要顯示的目前時間
                (20, 40),  # 指定文字左下角基準點座標
                cv2.FONT_HERSHEY_SIMPLEX,  # 指定文字字體
                0.7,  # 指定文字大小倍率
                (0, 255, 255),  # 指定文字顏色為黃色，OpenCV 使用 BGR 順序
                2,  # 指定文字線寬
                cv2.LINE_AA,  # 啟用抗鋸齒效果
            )  # 完成目前時間文字繪製
            cv2.putText(  # 將 FPS 與播放狀態繪製到畫面上
                frame,  # 指定要繪製文字的影片畫面
                fps_text,  # 指定要顯示的 FPS 與播放狀態
                (20, 70),  # 指定第二行文字左下角基準點座標
                cv2.FONT_HERSHEY_SIMPLEX,  # 指定文字字體
                0.7,  # 指定文字大小倍率
                (0, 255, 255),  # 指定文字顏色為黃色，OpenCV 使用 BGR 順序
                2,  # 指定文字線寬
                cv2.LINE_AA,  # 啟用抗鋸齒效果
            )  # 完成 FPS 文字繪製
            cv2.imshow(WINDOW_NAME, frame)  # 顯示目前影片畫面

            wait_time = 0 if is_paused else delay  # 暫停時等待按鍵，播放時依 FPS 等待
            key = cv2.waitKey(wait_time) & 0xFF  # 讀取鍵盤按鍵並保留按鍵的低 8 位元

            if key == ord("q"):  # 判斷使用者是否按下 q 鍵
                break  # 離開影片播放迴圈
            if key == ord(" "):  # 判斷使用者是否按下空白鍵
                is_paused = not is_paused  # 在暫停與播放狀態之間切換
    finally:  # 無論如何都執行影片資源清理
        capture.release()  # 釋放影片讀取資源
        cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗


def main() -> None:  # 定義程式主入口函式
    source = DEFAULT_SOURCE  # 設定預設 CCTV 串流來源
    if len(sys.argv) > 1:  # 檢查使用者是否提供影片路徑參數
        source = sys.argv[1]  # 使用命令列提供的影片檔案或串流網址
    play_video(source)  # 開始播放影片或 CCTV 串流


if __name__ == "__main__":  # 確認此檔案是直接執行
    main()  # 執行程式主入口

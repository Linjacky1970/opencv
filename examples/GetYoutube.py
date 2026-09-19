from __future__ import annotations  # 啟用較新的型別註記行為

import argparse  # 匯入命令列參數解析工具
import shutil  # 匯入尋找 FFmpeg 執行檔的工具
from pathlib import Path  # 匯入跨平台路徑工具

import imageio_ffmpeg  # 匯入提供專案內 FFmpeg 的套件
import yt_dlp  # 匯入 yt-dlp 下載套件
from yt_dlp.utils import DownloadError  # 匯入 yt-dlp 下載例外


PROJECT_ROOT = Path(__file__).resolve().parents[1]  # 取得專案根目錄
OUTPUT_DIRECTORY = PROJECT_ROOT / "video_output"  # 設定影片輸出目錄
DEFAULT_URL = "https://www.youtube.com/watch?v=COwra2aEzcg"  # 設定預設 YouTube 網址


def build_options(output_directory: Path) -> dict:  # 建立 yt-dlp 下載設定
    system_ffmpeg = shutil.which("ffmpeg")  # 嘗試尋找系統安裝的 FFmpeg
    ffmpeg_path = system_ffmpeg or imageio_ffmpeg.get_ffmpeg_exe()  # 找不到系統版本時使用套件內的 FFmpeg
    format_selector = "bv*+ba/b"  # 優先下載最佳影像與音訊，再退回最佳單一格式
    merge_format = "mp4"  # 將合併後的影片輸出為 MP4

    options = {  # 建立 yt-dlp 的完整設定字典
        "format": format_selector,  # 設定影片格式選擇規則
        "outtmpl": str(output_directory / "%(title)s [%(id)s].%(ext)s"),  # 設定輸出檔名與目錄
        "noplaylist": True,  # 只下載指定影片，不下載整個播放清單
        "paths": {"home": str(output_directory)},  # 將下載檔案寫入 video_output
        "quiet": False,  # 顯示下載進度
        "no_warnings": False,  # 保留必要的 yt-dlp 警告
        "js_runtimes": {"node": {}},  # 使用已安裝的 Node.js 執行 YouTube JavaScript
        "remote_components": ["ejs:github"],  # 允許下載 yt-dlp 官方 EJS solver
        "retries": 10,  # 網路失敗時最多重試十次
        "fragment_retries": 10,  # 影片分段下載失敗時最多重試十次
        "ffmpeg_location": str(Path(ffmpeg_path).parent),  # 指定 yt-dlp 使用的 FFmpeg 所在目錄
    }  # 完成 yt-dlp 設定
    options["merge_output_format"] = merge_format  # 將分離串流合併為 MP4
    return options  # 回傳下載設定


def download_video(video_url: str) -> None:  # 下載指定 YouTube 影片
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)  # 確保 video_output 目錄存在
    options = build_options(OUTPUT_DIRECTORY)  # 建立目前環境適用的下載設定
    print(f"開始下載：{video_url}")  # 顯示開始下載訊息
    print(f"輸出目錄：{OUTPUT_DIRECTORY}")  # 顯示實際輸出目錄

    try:  # 捕捉 yt-dlp 下載過程的例外
        with yt_dlp.YoutubeDL(options) as downloader:  # 建立 yt-dlp 下載器
            result = downloader.download([video_url])  # 開始下載指定 YouTube 影片
    except DownloadError as error:  # 捕捉 yt-dlp 下載或解析錯誤
        raise RuntimeError(f"YouTube 影片下載失敗：{error}") from error  # 回傳容易理解的錯誤

    if result != 0:  # 檢查 yt-dlp 是否回傳失敗狀態碼
        raise RuntimeError(f"yt-dlp 下載結束，但回傳錯誤碼：{result}")  # 回報下載失敗
    print("影片下載完成。")  # 顯示下載完成訊息


def parse_arguments() -> argparse.Namespace:  # 建立命令列參數解析器
    parser = argparse.ArgumentParser(description="下載 YouTube 影片到 video_output。")  # 建立參數解析器
    parser.add_argument("url", nargs="?", default=DEFAULT_URL, help="YouTube 影片 URL。")  # 接收指定的 YouTube URL
    return parser.parse_args()  # 回傳解析後的命令列參數


def main() -> None:  # 定義程式主入口
    arguments = parse_arguments()  # 取得命令列參數
    try:  # 捕捉程式層級的下載錯誤
        download_video(arguments.url)  # 下載使用者指定的影片
    except RuntimeError as error:  # 捕捉並顯示下載錯誤
        print(f"錯誤：{error}")  # 顯示錯誤原因
        raise SystemExit(1) from error  # 以失敗狀態結束程式


if __name__ == "__main__":  # 確認檔案是直接執行
    main()  # 執行程式主入口

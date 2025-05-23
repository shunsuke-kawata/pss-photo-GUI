import cv2
from datetime import datetime
import os
import shutil

def initialize_captures(root_folder_name):
    captures = []
    i = 0
    flag = True

    print("キャプチャデバイスの初期化を開始します...")
    while(flag):
        print(f"キャプチャデバイス{i}を試行中...")
        capture = cv2.VideoCapture(i)
        if not capture.isOpened():
            print(f"キャプチャデバイス{i}のオープンに失敗しました。")
            break
            

        # 画質を最大化する設定
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 解像度を1920x1080に設定
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        capture.set(cv2.CAP_PROP_FPS, 30) # フレームレートを30に設定（カメラによって異なる場合あり）

        # 設定後に解像度を確認
        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = capture.get(cv2.CAP_PROP_FPS)
        print(f"カメラ{i}: 解像度 {int(width)}x{int(height)}, FPS {int(fps)}")

        ret, _ = capture.read()
        flag = ret
        if flag:
            camera_name = f"camera{i}"
            folder_path = create_folder(root_folder_name, camera_name)
            tmp = {"index": i, "cap": capture, "camera_name": camera_name, "folder_path": folder_path}
            captures.append(tmp)
            i += 1
        else:
            print(f"キャプチャデバイス{i}からフレームの読み込みに失敗しました。")
    
    return captures

def create_folder(root_folder_name, camera_name):
    now = datetime.now()
    formatted_now = now.strftime('%Y%m%d_%H%M%S')
    folder_path = f"./{root_folder_name}/{camera_name}_{formatted_now}"
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def display_capture_frames(captures):
    print(f"接続台数：{len(captures)}")

    while(True):
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("終了")
            break
        
        now = datetime.now()
        formatted_now = now.strftime('%Y%m%d_%H%M%S')
        # 各キャプチャデバイスからフレームを取得して表示
        for i, capture in enumerate(captures):
            cap = capture["cap"]
            camera_name = capture["camera_name"]
            folder_path = capture["folder_path"]

            tmp_photo_name = f"{camera_name}_{formatted_now}.jpg"
            ret, frame = cap.read()
            if ret:
                cv2.imshow('frame' + str(i), frame)
            else:
                print(f"キャプチャデバイス{i}からフレームの読み込みに失敗しました。")
            
            # キャプチャを保存
            if(ret and key == ord('c')):
                cv2.imwrite(f"{folder_path}/{tmp_photo_name}", frame)
                print(f"キャプチャしました：{camera_name}")
                del ret, frame

def release_resources(captures):
    for capture in captures:
        cap = capture["cap"]
        cap.release()
    cv2.destroyAllWindows()

def main():
    """メイン関数"""
    now = datetime.now()
    formatted_now = now.strftime('%Y%m%d_%H%M%S')
    root_folder_name = f"result_{formatted_now}"
    os.makedirs(root_folder_name, exist_ok=True)
    captures = initialize_captures(root_folder_name)  # キャプチャデバイスの初期化

    # 接続された機器が存在しないとき結果ディレクトリを削除
    if(len(captures) == 0):
        print("接続されているデバイスがありません")
        shutil.rmtree(root_folder_name)
        return
    
    display_capture_frames(captures)  # フレームの表示
    release_resources(captures)  # リソースの解放

if __name__ == "__main__":
    main()

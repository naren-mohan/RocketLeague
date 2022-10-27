from fileinput import filename
import time
import win32gui, win32ui, win32con, win32api
import os
import pylink
from PIL import Image
import concurrent.futures

def compress(bmpstr, filename):
    global w, h
    im = Image.frombuffer(
        'RGB', (w, h), bmpstr, 'raw', 'BGRX', 0, 1)
    im.save(filename, quality=30)    

def window_capture():
    global w, h
    hwnd = 0 
    hwndDC = win32gui.GetWindowDC(hwnd)
    try:
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    except:
        print(mfcDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h) , mfcDC, (0, 0), win32con.SRCCOPY)
    # rtns = saveBitMap.GetBitmapBits(True)
    # bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    return bmpstr

def record_window():
    i = 0
    timestamp = time.time()
    try:    
        while True:
            window_capture("Capture\\"+ str(i) +".jpg")
            i+=1
    except KeyboardInterrupt:
        print(i)
        print("Time: {}".format( round(time.time() - timestamp, 2)))

if __name__ == '__main__':
    results_folder = 'Capture'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    
    # Get width and the height of the screen
    w, h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        i = 0
        start_time = time.time()
        try:
            while True:
                bmpstr = window_capture()
                futures.append(executor.submit(compress, bmpstr=bmpstr, filename=results_folder+"\\"+str(i)+".jpg"))
                i += 1
        except KeyboardInterrupt:
            print(i)
            print(round(time.time() - start_time, 2))

        #     # print(len(concurrent.futures.as_completed(futures)))
        # except Exception as E:
        #     print


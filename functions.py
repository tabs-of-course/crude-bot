import cv2
from time import sleep
import ctypes
import numpy as np
import win32ui
import win32api
import win32gui
import win32con
import pyautogui
from skimage import metrics
from settings import *


def left_click(hwnd, x, y, delay):
    # 33 pixel offset to account for the top bar
    lParam = win32api.MAKELONG(x, y - 33)
    win32gui.SendMessage(
        hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    sleep(delay)
    win32gui.SendMessage(
        hwnd, win32con.WM_LBUTTONUP, 0, lParam)


def current_mouse_pos(hwnd):
    pos = pyautogui.position()
    return win32gui.ScreenToClient(hwnd, pos)


def find_sprite(hwnd, sprite_path):
    x = 0
    y = 0
    gray_img = make_gray_image(get_background_screen(hwnd))
    threshold = 0.9
    sprite_sprite = cv2.imread(sprite_path, 0)
    sprite_sprite_w, sprite_sprite_h = sprite_sprite.shape[::-1]
    res = cv2.matchTemplate(gray_img, sprite_sprite, cv2.TM_CCOEFF_NORMED)
    sprite_sprite_loc = np.where(res >= threshold)
    a = np.array(sprite_sprite_loc)
    try:
        coord = a[:, 0]
        x = coord[1]
        y = coord[0]
    except:
        x = 0
        y = 0
    return(x, y)


def make_gray_image(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)


def getSpecificHWND(window):
    hwnd = win32gui.FindWindow(0, window)
    return hwnd


def get_child_windows(parent):
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(
        parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList


def get_background_screen(hwnd):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Black screen without this line
    ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpInfo = saveBitMap.GetInfo()
    bmpStr = saveBitMap.GetBitmapBits(True)
    img = np.frombuffer(saveBitMap.GetBitmapBits(True), dtype=np.uint8)
    img.shape = (h, w, 4)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    return img


def find_diff(hwnd):

    # Take 3 consecutive screenshots
    pic_1 = get_background_screen(hwnd)
    sleep(0.13)
    pic_2 = get_background_screen(hwnd)
    sleep(0.13)
    pic_3 = get_background_screen(hwnd)

    # Convert images to grayscale
    pic_1_gray = cv2.cvtColor(pic_1, cv2.COLOR_BGR2GRAY)
    pic_2_gray = cv2.cvtColor(pic_2, cv2.COLOR_BGR2GRAY)
    pic_3_gray = cv2.cvtColor(pic_3, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between images
    (score_1_2, diff_1_2) = metrics.structural_similarity(
        pic_1_gray, pic_2_gray, full=True)
    (score_2_3, diff_2_3) = metrics.structural_similarity(
        pic_2_gray, pic_3_gray, full=True)
    (score, diff) = metrics.structural_similarity(
        diff_1_2, diff_2_3, full=True)
    # print("Image similarity", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # diff_1_2 = (diff_1_2 * 255).astype("uint8")
    # cv2.imwrite('images/diff_1_2.jpg', diff_1_2)

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(
        diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    contours = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = contours[0] if len(contours) == 2 else contours[1]

    x = 0
    y = 0
    mobs_pos = []

    for c in contours:
        area = cv2.contourArea(c)
        if 555 < area:
            x, y, w, h = cv2.boundingRect(c)
            if x in range(p_b_loc[0] - p_b_loc_offset, p_b_loc[0] + p_b_loc_offset)                 \
                    and y in range(p_b_loc[1] - p_b_loc_offset, p_b_loc[1] + p_b_loc_offset)        \
                    or x in range(p_c_loc[0] - p_c_loc_offset_neg, p_c_loc[0] + p_c_loc_offset_pos) \
                    and y in range(p_c_loc[1] - p_c_loc_offset_neg, p_c_loc[1] + p_c_loc_offset_pos):

                cv2.rectangle(
                    pic_3, (x, y), (x + w, y + h), (0, 355, 64), 2)
            else:
                mobs_pos.append(cv2.boundingRect(c))
                cv2.rectangle(
                    pic_3, (x, y), (x + w, y + h), (1, 56, 248), 2)
                cv2.circle(
                    pic_3, (x + int(w/2), y + int(h/2)), 1, (255, 255, 255), 10)
                cv2.circle(
                    pic_3, (x + int(w/2), y + int(h/2)), 1, (0, 0, 0), 5)

            cv2.imwrite('images/after.jpg', pic_3)
            cv2.imwrite('images/diff.jpg', diff)
        # else:

        #     x, y, w, h = cv2.boundingRect(c)
        #     cv2.rectangle(
        #         pic_3, (x, y), (x + w, y + h), (255, 255, 255), 2)
    return mobs_pos

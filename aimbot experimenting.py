import cv2
import numpy as np
import pyautogui
import mss  # Faster than PIL
import time

# Screen region around crosshair (adjust for your res)
monitor = {"left": 800, "top": 500, "width": 320, "height": 200}

def detect_red(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Red exists at both ends of HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 100:  # Minimum size filter
            x, y, w, h = cv2.boundingRect(largest)
            return (x + w // 2, y + h // 2)
    return None

with mss.mss() as sct:
    while True:
        img = np.array(sct.grab(monitor))
        target = detect_red(img)
        
        if target:
            # Convert relative to screen coords
            screen_x = monitor["left"] + target[0]
            screen_y = monitor["top"] + target[1]
            
            # Humanized movement (0.2s duration)
            pyautogui.moveTo(screen_x, screen_y, duration=0.2)
            pyautogui.click()

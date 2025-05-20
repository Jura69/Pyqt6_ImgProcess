import numpy as np
import cv2

def image_scaling(image, max_width=650, max_height=650):
    h, w = image.shape[:2]
    scaleX = max_width / w
    scaleY = max_height / h
    scale = min(scaleX, scaleY)
    if scale == 1:
        return image  # Không cần scale
    new_w = int(w * scale)
    new_h = int(h * scale)
    M = np.float32([[scale, 0, 0], [0, scale, 0]])
    return cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_LINEAR) 
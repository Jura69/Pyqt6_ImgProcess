import numpy as np
import cv2

def image_scaling(image, max_width=600, max_height=600):
    h, w = image.shape[:2]
    scaleX = min(1, max_width / w)
    scaleY = min(1, max_height / h)
    scale = min(scaleX, scaleY)
    if scale == 1:
        return image  # Không cần scale
    new_w = int(w * scale)
    new_h = int(h * scale)
    M = np.float32([[scale, 0, 0], [0, scale, 0]])
    return cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_LINEAR) 
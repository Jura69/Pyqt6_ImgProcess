import numpy as np
import cv2

def average_filter(img, kernel_size=3):
    '''Lọc trung bình với kernel size tùy chỉnh
    
    Công thức toán học:
    g(x,y) = (1/k²) * Σ(i=0 to k-1) Σ(j=0 to k-1) f(x+i, y+j)
    
    Trong đó:
    - g(x,y): giá trị pixel đầu ra tại vị trí (x,y)
    - f(x,y): giá trị pixel đầu vào tại vị trí (x,y)
    - k: kích thước kernel (k x k)
    - (1/k²): hệ số chuẩn hóa
    
    Ví dụ với kernel 3x3:
    g(x,y) = (1/9) * [
        f(x-1,y-1) + f(x-1,y) + f(x-1,y+1) +
        f(x,y-1)   + f(x,y)   + f(x,y+1)   +
        f(x+1,y-1) + f(x+1,y) + f(x+1,y+1)
    ]
    
    Tham số:
        img: Ảnh đầu vào (phải là ảnh màu)
        kernel_size: Kích thước kernel (phải là số lẻ)
    Trả về:
        Ảnh đã được lọc trung bình
    '''
    # Tính offset cho kernel
    offset = kernel_size // 2
    m, n = img.shape[:2]
    img_new = np.zeros_like(img)
    
    # Tính hệ số chuẩn hóa
    normalization = 1.0 / (kernel_size * kernel_size)
    
    # Xử lý cho ảnh màu (3 kênh)
    for channel in range(img.shape[2]):
        for i in range(offset, m - offset):
            for j in range(offset, n - offset):
                # Lấy vùng kernel
                kernel = img[i-offset:i+offset+1, j-offset:j+offset+1, channel]
                # Tính trung bình và nhân với hệ số chuẩn hóa
                img_new[i, j, channel] = np.sum(kernel) * normalization
    
    return img_new 
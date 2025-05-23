import numpy as np
import cv2

def median_filter(img, kernel_size=3):
    '''Lọc trung vị với kernel size tùy chỉnh
    
    Công thức toán học:
    g(x,y) = median(f(x+i,y+j)) với i,j trong kernel
    
    Trong đó:
    - g(x,y): giá trị pixel đầu ra tại vị trí (x,y)
    - f(x,y): giá trị pixel đầu vào tại vị trí (x,y)
    
    Ví dụ với kernel 3x3:
    g(x,y) = median{
        f(x-1,y-1), f(x-1,y), f(x-1,y+1),
        f(x,y-1),   f(x,y),   f(x,y+1),
        f(x+1,y-1), f(x+1,y), f(x+1,y+1)
    }
    
    Tham số:
        img: Ảnh đầu vào (phải là ảnh màu)
        kernel_size: Kích thước kernel (phải là số lẻ)
    Trả về:
        Ảnh đã được lọc trung vị
    '''
    # Tính offset cho kernel
    offset = kernel_size // 2
    m, n = img.shape[:2]
    img_new = np.zeros_like(img)
    
    # Xử lý cho ảnh màu (3 kênh)
    for channel in range(img.shape[2]):
        for i in range(offset, m - offset):
            for j in range(offset, n - offset):
                # Lấy vùng kernel
                kernel = img[i-offset:i+offset+1, j-offset:j+offset+1, channel]
                # Sắp xếp và lấy giá trị trung vị
                temp = sorted(kernel.flatten())
                img_new[i, j, channel] = temp[len(temp)//2]
    
    return img_new 
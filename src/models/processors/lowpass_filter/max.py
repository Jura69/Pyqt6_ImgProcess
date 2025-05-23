import numpy as np

def max_filter(img, kernel_size=3):
    '''Lọc max với kernel size tùy chỉnh
    
    Công thức toán học:
    g(x,y) = max(f(x+i,y+j)) với i,j trong kernel
    
    Trong đó:
    - g(x,y): giá trị pixel đầu ra tại vị trí (x,y)
    - f(x,y): giá trị pixel đầu vào tại vị trí (x,y)
    
    Ví dụ với kernel 3x3:
    g(x,y) = max{
        f(x-1,y-1), f(x-1,y), f(x-1,y+1),
        f(x,y-1),   f(x,y),   f(x,y+1),
        f(x+1,y-1), f(x+1,y), f(x+1,y+1)
    }
    
    Tham số:
        img: Ảnh đầu vào (phải là ảnh màu)
        kernel_size: Kích thước kernel (phải là số lẻ)
    Trả về:
        Ảnh đã được lọc max
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
                # Lấy giá trị lớn nhất
                img_new[i, j, channel] = np.max(kernel)
    
    return img_new 
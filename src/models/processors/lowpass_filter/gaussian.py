import numpy as np

def gaussian_filter(img, kernel_size=3):
    '''Lọc Gaussian với kernel size tùy chỉnh
    
    Công thức toán học:
    G(x,y) = (1/(2πσ²)) * e^(-(x²+y²)/(2σ²))
    
    Trong đó:
    - G(x,y): giá trị kernel tại vị trí (x,y)
    - σ: độ lệch chuẩn (standard deviation)
    - x,y: tọa độ tương đối so với tâm kernel
    
    Ví dụ với kernel 3x3 (σ = 1):
    Kernel = (1/16) * [
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ]
    
    Tham số:
        img: Ảnh đầu vào (phải là ảnh màu)
        kernel_size: Kích thước kernel (phải là số lẻ)
    Trả về:
        Ảnh đã được lọc Gaussian
    '''
    # Tính độ lệch chuẩn dựa trên kernel size
    sigma = 0.3 * ((kernel_size - 1) * 0.5 - 1) + 0.8
    
    # Tạo ma trận tọa độ
    ax = np.linspace(-(kernel_size - 1) / 2., (kernel_size - 1) / 2., kernel_size)
    xx, yy = np.meshgrid(ax, ax)
    
    # Tính kernel Gaussian
    kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sigma))
    kernel = kernel / np.sum(kernel)  # Chuẩn hóa kernel
    
    # Tính offset cho kernel
    offset = kernel_size // 2
    m, n = img.shape[:2]
    img_new = np.zeros_like(img)
    
    # Xử lý cho ảnh màu (3 kênh)
    for channel in range(img.shape[2]):
        for i in range(offset, m - offset):
            for j in range(offset, n - offset):
                # Lấy vùng kernel
                region = img[i-offset:i+offset+1, j-offset:j+offset+1, channel]
                # Áp dụng convolution
                img_new[i, j, channel] = np.sum(region * kernel)
    
    return img_new 
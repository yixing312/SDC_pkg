import cv2
import matplotlib.pyplot as plt

# 读取文件
file_path = '../data/error_out.out'
with open(file_path, 'r') as file:
    lines = file.readlines()

# 逐行输出视频
for i, line in enumerate(lines):
    # 分割每一行的六个量
    values = line.strip().split(',')
    x_values = []
    y_values = []
    z_values = []
    ox_values = []
    oy_values = []
    oz_values = []
    if len(values) >= 6:
        x_values.append(float(values[0]))
        y_values.append(float(values[1]))
        z_values.append(float(values[2]))
        ox_values.append(float(values[3]))
        oy_values.append(float(values[4]))
        oz_values.append(float(values[5]))
    plt.plot(x_values, label="X")
    plt.plot(y_values, label="Y")
    plt.plot(z_values, label="Z")
    plt.legend()
    plt.savefig("../data/error_out_possion.png")
    frame = cv2.imread("../data/error_out_possion.png") 

    # 绘制折线图像
    plt.plot(range(i*10, i*10+10), values[:i+1])

    # 显示视频帧和折线图像
    plt.imshow(frame)
    plt.show()

# 释放资源
cv2.destroyAllWindows()

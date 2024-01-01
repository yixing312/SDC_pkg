import matplotlib.pyplot as plt

# Read the file
file_path = "../data/error_out.out"
with open(file_path, "r") as file:
    lines = file.readlines()

# Extract the values
x_values = []
y_values = []
z_values = []
for line in lines:
    values = line.strip().split(",")
    if len(values) >= 3:
        x_values.append(float(values[0]))
        y_values.append(float(values[1]))
        z_values.append(float(values[2]))

# Plot the values
plt.plot(x_values, label="X")
plt.plot(y_values, label="Y")
plt.plot(z_values, label="Z")
plt.legend()
plt.savefig("../data/error_out_possion.png")
# plt.show()

plt.cla()

# 将后三个值作为角度绘制在另外一张图上
ox_values = []
oy_values = []
oz_values = []
for line in lines:
    values = line.strip().split(",")
    if len(values) >= 3:
        ox_values.append(float(values[3]))
        oy_values.append(float(values[4]))
        oz_values.append(float(values[5]))

# Plot the values
plt.plot(ox_values, label="OX")
plt.plot(oy_values, label="OY")
plt.plot(oz_values, label="OZ")
plt.legend()
plt.savefig("../data/error_out_angle.png")
# plt.show()

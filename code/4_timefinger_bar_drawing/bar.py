import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

output_path = 'time_bar.eps'
# 定义颜色渐变和图像大小
num_points = 100  # 渐变中的颜色点数，增加这个值会使渐变更平滑
gradient = np.linspace(1, 0, num_points).reshape(1, num_points)  # 从蓝色到红色
figsize = (6, 1)  # 色标的尺寸，可根据需要调整

# 创建色板
cmap = sns.color_palette("RdBu", as_cmap=True)

# 创建图形并添加色标
fig, ax = plt.subplots(figsize=figsize)
ax.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 1, 0, 1])

# 添加坐标轴刻度和标签
ax.set_yticks([])  # 通常色标不需要 y 轴刻度，但您可以自定义
ax.set_xticks([0, 1])  # 在色标的开始、中间和结束位置设置 x 轴刻度
ax.set_xticklabels([0,  2600])  # 根据需要设置 x 轴刻度标签
ax.set_xlabel('Seconds')  # 给 x 轴添加标签，表示色标代表的意义

plt.savefig(output_path,dpi=600,bbox_inches='tight')
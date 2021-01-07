# @Author: vancece(连梓煜)
from readCsv import readCsv
import matplotlib.pyplot as plt
import math
import numpy as np


def corrcoef(x, y=None, rowvar=True):
    c = np.cov(x, y, rowvar)
    try:
        d = np.diag(c)
    except ValueError:
        # scalar covariance
        # nan if incorrect value (nan, inf, 0), 1 otherwise
        return c / c
    stddev = np.sqrt(d.real)
    c /= stddev[:, None]
    c /= stddev[None, :]

    np.clip(c.real, -1, 1, out=c.real)
    if np.iscomplexobj(c):
        np.clip(c.imag, -1, 1, out=c.imag)

    return c


# 获取平均值
def get_average(list):
    return sum(list) / len(list)


# 获取方差
def get_variance(list):
    average = get_average(list)
    return sum([(x - average) ** 2 for x in list]) / len(list)


# 求数组标准差
def get_standard_deviation(list):
    variance = get_variance(list)
    return math.sqrt(variance)


# 求数组的z-score归一化最后的结果
def get_z_score(list):
    avg = get_average(list)
    stan = get_standard_deviation(list)
    scores = [(i - avg) / stan for i in list]
    return scores


# 1. 请以课程1成绩为x轴，体能成绩为y轴，画出散点图。
def drawScatter(csv_data):
    # matplotlib画图中中文显示会有问题，需要这两行设置默认字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 画两条（0-9）的坐标轴并设置轴标签x，y
    plt.xlim(xmax=100, xmin=0)
    plt.ylim(ymax=100, ymin=0)

    # 设置标签
    plt.xlabel("课程1成绩")
    plt.ylabel("体能成绩")

    # 画散点图
    plt.scatter(csv_data["C1"], csv_data["Constitution"])

    plt.show()


# 2. 以5分为间隔，画出课程1的成绩直方图。
def drawHits(csv_data):
    # matplotlib画图中中文显示会有问题，需要这两行设置默认字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 画两条（0-9）的坐标轴并设置轴标签x，y
    plt.xlim(xmax=100, xmin=60)

    # 设置标签
    plt.xlabel("课程1成绩")
    plt.ylabel("人数")

    # 设置区间
    plt.xticks(range(0, 100, 5))

    # 定义间隔大小
    space_between = 5
    # 区间个数
    bins = int((max(csv_data["C1"]) - min(csv_data["C1"])) / space_between)

    # 绘制直方图
    plt.hist(csv_data["C1"], bins=bins, align='mid')

    plt.show()


# 3. 对每门成绩进行z-score归一化，得到归一化的数据矩阵。
def normalization(csv_data):
    for column in ['C1', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'Constitution']:
        csv_data[column] = get_z_score(csv_data[column])

    return csv_data


# 4. 计算出100x100的相关矩阵，并可视化出混淆矩阵。（为避免歧义，这里“协相关矩阵”进一步细化更正为100x100的相关矩阵，100为学生样本数目，视实际情况而定）
def calcular_relate_arr(csv_data):
    resource = [csv_data['C1'], csv_data['C2'], csv_data['C3'], csv_data['C4'], csv_data['C5'], csv_data['C6'],
                csv_data['C7'], csv_data['C8'], csv_data['C9'], csv_data['Constitution']]
    result = corrcoef(resource)
    return result


# 5. 根据相关矩阵，找到距离每个样本最近的三个样本，得到100x3的矩阵（每一行为对应三个样本的ID）输出到txt文件中，以\t,\n间隔。


if __name__ == '__main__':
    csv_data = readCsv("../resource.csv")
    print(csv_data)
    drawScatter(csv_data)
    drawHits(csv_data)

    calcular_relate_arr(csv_data)

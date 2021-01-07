import csv
import xlrd
import process_1

"""
1、读取数据
2、数据处理，对两个数据源的一致性合并
3、每个学生样本的数值量化
    1. 学生中家乡在Beijing的所有课程的平均成绩。
    2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。(备注：该处做了修正，课程10数据为空，更改为课程9)
    3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
    4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）
"""

# 读取txt文件数据
data = []
try:
    f = open("C:\\Users\\WK\\Desktop\\ML_DM\\data_source\\txtdata.txt", 'r')
    all_lines = f.readlines()
    for line in all_lines:
        line = line.strip().split(',')
        if line[0] != 'ID':
            line[0] = float(line[0]) - 202000
            if line[3] == 'male':
                line[3] = 'boy'
            if line[3] == 'female':
                line[3] = 'girl'
            for i in range(11):
                if line[i + 4] != '':
                    line[i + 4] = float(line[i + 4])
                else:
                    line[i + 4] = 'NULL'
            if line[4] != 'NULL':
                line[4] = line[4] * 100.0
            if line[15] == '':
                line[15] = 'NULL'

        data.append(line)
finally:
    f.close()
    # print(len(data))
    # print(data[1])
# 读取xlsx文件数据


xlsx_data = xlrd.open_workbook("C:\\Users\\WK\\Desktop\\ML_DM\\data_source\\xlsxdata.xlsx")  ##获取文本对象
table = xlsx_data.sheets()[0]  # 根据index获取某个sheet
rows = table.nrows  # 3获取当前sheet页面的总行数,把每一行数据作为list放到 list
try:
    for i in range(rows):
        col = table.row_values(i)  # 获取每一列数据
        # print(col)
        if col[0] != 'ID':
            if col[3] == 'male':
                col[3] = 'boy'
            if col[3] == 'female':
                col[3] = 'girl'
            for i in range(11):
                if col[i + 4] == '':
                    col[i + 4] = 'NULL'
            if col[15] == '':
                col[15] = 'NULL'
        data.append(col)
except:
    print("读取失败")
else:
    print("读取成功，数据总数：", len(data))

# 1）、去重
d = []
dd = []  # 放着重复的
for i in data:
    if i not in d:
        d.append(i)
    else:
        dd.append(i)

end = []
ed = []
end.append(d[0])
ed.append(d[0])

# print("d", len(d))
# print("dd", len(dd))
# print("len(data)1", len(data))

#去除不完全一致，但代表相同的数据
def check(i_line):
    count = []
    # print(end)
    for end_i in end:
        cou = 0
        for k in range(len(end_i)):
            if i_line[k] == end_i[k]:
                cou = cou + 1
        count.append(cou)
    return count


for i in d:
    if i[0] != 'ID':
        ckeck = check(i)
        flag = 0
        for k in range(len(ckeck)):
            if ckeck[k] > 8:
                flag = flag + 1
        if flag == 0:
            end.append(i)
        else:
            ed.append(i)

# print("len(end)", len(end))
data = end

del data[0]
# print("len(data)2", len(data))
score = []  # 每列成绩的总和
flag = []  # 实际计算的人数，除了NULL
averge = []  # 平均值

# 九门课分别的总和,self.score = []
for i in range(5, 14):
    sc = 0
    fl = 0
    for line in data:
        if line[i] != 'NULL':
            fl = fl + 1
            sc = sc + line[i]
    score.append(sc)
    averge.append(sc / fl)

sc = 0
fl = 0
s = 0
# 体能测试成绩的总和
for line in data:

    if line[15] != 'NULL':
        fl = fl + 1
        if line[15] == 'excellent':
            sc = sc + 100
        elif line[15] == 'good':
            sc = sc + 80
        elif line[15] == 'general':
            sc = sc + 60
        elif line[15] == 'bad':
            sc = sc + 40
score.append(sc)
flag.append(fl)
averge.append(sc / fl)

# 保存数据,将空值置为均值
for i in range(5, 14):
    for line in end:
        if line[i] == 'NULL':
            line[i] = averge[i - 5]
for line in end:
    if line[15] == 'NULL':
        line[15] = 'general'


# 获取列表的第1个元素，序号
def takesecond(elem):
    return int(elem[0])

# 指定第1个元素排序，按序号进行升序排序
end.sort(key=takesecond)

f = open('data.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['ID', 'Name', 'City', 'Gender', 'Height', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                 'Constitution'])
for i in end:
    writer.writerow(i)
f.close()
print("数据处理结束")
pro = process_1.Process()
pro.run()



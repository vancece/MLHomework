import csv
import math


class Process:

    def __init__(self):
        self.data = []
        self.score = []  # 每列成绩的总和
        self.averge = []  # 平均值
        self.standard_dev = []  # 标准差
        self.result = []  # 相关系数

    # 读取xlsx文件数据
    def reader(self):
        try:
            f = open('data.csv', 'r', newline='')
            reader = csv.reader(f)
        except:
            print("文件读取失败")
        else:
            for line in reader:
                if line[0] != 'ID':
                    for i in range(10):
                        line[i + 4] = float(line[i + 4])

                self.data.append(line)
            f.close()

        del self.data[0]
        # print(len(self.data))
        # print(self.data[1])

    # 1. 学生中家乡在Beijing的所有课程的平均成绩。
    def beijing(self):
        sco = []
        for line in self.data:
            flag = 0
            total = 0
            if line[2] == 'Beijing':
                for k in range(5, 14):
                    flag = flag + 1
                    total = total + line[k]
                sco.append((total / flag))
        # print(sco)
        print("1、学生中家乡在Beijing的所有课程的平均成绩:")
        print(sco)
        # for id in range(len(sco)):
        #     print("C%d:" % (id + 1), "%.2f" % sco[id])


    # 2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。(备注：该处做了修正，课程10数据为空，更改为课程9)
    def guangzhou(self):
        flag = 0
        for line in self.data:
            if line[2] == 'Guangzhou' and line[3] == 'boy' and line[5] != 'NULL' and line[13] != 'NULL':
                if line[5] > 80 and line[13] > 9:
                    flag = flag + 1
        print("2、学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量:", flag)

    # 3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
    def physical(self):
        flag_gz = 0
        flag_sh = 0
        guangzhou = 0
        shanghai = 0
        for line in self.data:
            if line[2] == 'Guangzhou' and line[3] == 'girl':
                flag_gz = flag_gz + 1
                if line[15] == 'excellent':
                    guangzhou = guangzhou + 100
                elif line[15] == 'good':
                    guangzhou = guangzhou + 80
                elif line[15] == 'general':
                    guangzhou = guangzhou + 60
                elif line[15] == 'bad':
                    guangzhou = guangzhou + 40
            elif line[2] == 'Shanghai' and line[3] == 'girl':
                flag_sh = flag_sh + 1
                if line[15] == 'excellent':
                    shanghai = shanghai + 100
                elif line[15] == 'good':
                    shanghai = shanghai + 80
                elif line[15] == 'general':
                    shanghai = shanghai + 60
                elif line[15] == 'bad':
                    shanghai = shanghai + 40
        guangzhou = guangzhou / flag_gz
        shanghai = shanghai / flag_sh
        if guangzhou > shanghai:
            print("2、广州地区女生的平均体能测试成绩更强")
        elif shanghai > guangzhou:
            print("2、上海地区女生的平均体能测试成绩更强")
        else:
            print("2、二者势均力敌")

    # 4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）
    def dependency(self):
        # 九门课分别的总和,self.score = []
        for i in range(5, 14):
            sc = 0
            for line in self.data:
                sc = sc + line[i]
            self.score.append(sc)
            self.averge.append(sc / len(self.data))

        # 标准差
        for i in range(5, 14):
            s = 0
            for line in self.data:
                s += pow(line[i] - (self.averge[i - 5]), 2)
            s = s / (len(self.data) - 1)
            s = math.sqrt(s)
            self.standard_dev.append(s)

        sc = 0

        # 体能测试成绩的总和
        for line in self.data:
            if line[15] == 'excellent':
                sc = sc + 100
            elif line[15] == 'good':
                sc = sc + 80
            elif line[15] == 'general':
                sc = sc + 60
            elif line[15] == 'bad':
                sc = sc + 40
        self.score.append(sc)
        self.averge.append(sc / len(self.data))

        s = 0
        for line in self.data:
            if line[15] == 'excellent':
                s = s + pow(100 - (sc / len(self.data)), 2)
            elif line[15] == 'good':
                s = s + pow(80 - (sc / len(self.data)), 2)
            elif line[15] == 'general':
                s = s + pow(60 - (sc / len(self.data)), 2)
            elif line[15] == 'bad':
                s = s + pow(40 - (sc / len(self.data)), 2)
        s = s / len(self.data)
        s = math.sqrt(s)
        self.standard_dev.append(s)

        # print("每列成绩总和:", '\n', self.score)
        # print("每列均值", '\n', self.averge)
        # print("每列标准差", '\n', self.standard_dev)

        _EXY = []
        # E(XY)
        for i in range(5, 14):
            s = 0
            c = 0
            for line in self.data:
                if line[15] == 'excellent':
                    c = line[i] * 100
                elif line[15] == 'good':
                    c = line[i] * 80
                elif line[15] == 'general':
                    c = line[i] * 60
                elif line[15] == 'bad':
                    c = line[i] * 40
                s = s + c
            _EXY.append(s / len(self.data))

        # 协方差cov(X,Y) = E(XY)- E(X)*E(Y)
        cov = []
        for i in range(len(_EXY)):
            cov.append(_EXY[i] - self.averge[i] * self.averge[-1])
        #print("协方差cov(X,Y)", '\n', cov)
        # 相关系数
        for i in range(len(cov)):
            self.result.append(cov[i] / (self.standard_dev[i] * self.standard_dev[-1]))
        print("4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）")
        for k in range(len(self.result)):
            print("C%d"%(k+1),"与体能成绩相关系数为：", self.result[k])


    def run(self):
        self.reader()
        self.beijing()
        self.guangzhou()
        self.physical()
        self.dependency()


if __name__ == '__main__':
    pro = Process()
    pro.run()

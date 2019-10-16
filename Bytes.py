class Byte:
    def __init__(self):
        #无参数初始化
        self.bits = [0,0,0,0,0,0,0,0]
        self.d = 0
    def __init__(self,n:int):
        #指定整型初始化
        if not type(n) is int: raise TypeError
        #判断数据溢出
        if n > 127 or n < -128: raise TypeError("Data Overflowed")

        if n >= 0:
            self.d = n
            s = bin(n)[2:]
            while len(s) < 7: s = '0' + s #补0
            #正整数转换七位二进制存入，符号位填0
            self.bits = [0] + [int(i) for i in s]
        else:
            self.d = n
            self.bits = []
            s = bin(-n)[2:]
            while len(s) < 7: s = '0' + s #取绝对值补位
            s = [1 if i == '0' else 0 for i in s] #取反码，字符转数字
            p = True #进位指示，加一初始化
            for i in s[::-1]: #取逆序进行加法
                if i == 0 and p: #逢0加1，进位结束
                    self.bits.append(1)
                    p = False
                    continue
                if i == 0:
                    self.bits.append(0)
                    continue
                if i == 1 and p: #遇1进1，添0，继续进位
                    self.bits.append(0)
                    continue
                if i == 1:
                    self.bits.append(1)
                    continue
            if len(self.bits) == 8:
                #若为-128,不用补位，逆回原序
                self.bits = self.bits[::-1]
            else:
                #符号位填1
                self.bits = [1] + self.bits[::-1]
            

    def show(self):
        print(f"Byte Data of {self.d}:  \t{self.bits}")

    def add(self, right, showProcess = True):
        if showProcess: print(f"\t{self.bits}\n+\t{right.bits}\n{'_'*40}")
        s = [] #结果Byte
        p = False #进位指示
        for l,r in zip(self.bits[::-1],right.bits[::-1]):
            #全加器逻辑
            if not p and l+r == 0:
                s.append(0)
                continue
            if not p and l*r == 0:
                s.append(1)
                continue
            if not p and l*r == 1:
                s.append(0)
                p = True
                continue
            if p and l+r == 0:
                s.append(1)
                p = False
                continue
            if p and l*r == 0:
                s.append(0)
                continue
            if p and l*r == 1:
                s.append(1)
                continue
        s = s[::-1] #逆回原序
        print("\t",s)
        if showProcess:
            #转回原码
            n = 0
            if s[0] == 0:#j结果大于等于0
                n = sum([k*2**i for i,k in enumerate((s[1:])[::-1])])
            else:
                s1 = [1 if i == 0 else 0 for i in s[1::][::-1]]#再进行反码加一操作转换回源码
                p = True #进位指示，加一初始化
                res = []
                for i in s1: 
                    if i == 0 and p: #逢0加1，进位结束
                        res.append(1)
                        p = False
                        continue
                    if i == 0:
                        res.append(0)
                        continue
                    if i == 1 and p: #遇1进1，添0，继续进位
                        res.append(0)
                        continue
                    if i == 1:
                        res.append(1)
                        continue
                n = -sum([k*2**i for i,k in enumerate(res)])
            print(f"Nominal Answer: {self.d + right.d}\nReal Answer: {n}\n{'Overflowed!' if self.d+right.d != n else ''}")
            
            
if __name__ == '__main__':
    for i in range(-128,128):
        Byte(i).show()
    print()
    Byte(34).add(Byte(66))
    Byte(12).add(Byte(-12))
    Byte(127).add(Byte(-128))
    Byte(100).add(Byte(100))
    Byte(-128).add(Byte(-1))

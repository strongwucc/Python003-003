import threading
import time
import queue

'''
哲学家吃饭
no 哲学家编号
limitNum 哲学家需要吃饭的次数
leftLock 哲学家左边的叉
rightLock 哲学家右边的叉
records 哲学家记录队列
'''


class DiningPhilosopher(threading.Thread):

    def __init__(self, no, limitNum, leftLock, rightLock, records):
        super().__init__()
        self.no = no
        self.leftLock = leftLock
        self.rightLock = rightLock
        self.eatNum = 0
        self.limitNum = limitNum
        self.records = records

    def run(self):

        print(f'编号为{self.no}的哲学家开始任务')

        while self.eatNum < self.limitNum:

            # 思考
            self.think()

            # 是否可以拿起左叉
            self.leftLock.acquire()
            self.pickLeftFork()

            # 是否可以拿起右叉
            self.rightLock.acquire()
            self.pickRightFork()

            # 吃饭
            self.eat()

            # 放下左叉
            self.putLeftFork()
            self.leftLock.release()

            # 放下右叉
            self.putRightFork()
            self.rightLock.release()

        print(f'编号为{self.no}的哲学家完成任务')

    # 思考
    def think(self):
        print(f'编号为{self.no}的哲学家正在思考...')
        time.sleep(1)
        print(f'编号为{self.no}的哲学家结束思考，准备吃第{self.eatNum + 1}次饭...')

    # 拿左边的叉
    def pickLeftFork(self):
        print(f'编号为{self.no}的哲学家拿起左边的叉...')
        self.records.put([self.no, 1, 1])

    # 拿右边的叉
    def pickRightFork(self):
        print(f'编号为{self.no}的哲学家拿起右边的叉...')
        self.records.put([self.no, 2, 1])

    # 吃饭
    def eat(self):
        print(f'编号为{self.no}的哲学家正在吃饭...')
        time.sleep(1)
        self.records.put([self.no, 0, 3])
        self.eatNum += 1

    # 放下左边的叉
    def putLeftFork(self):
        print(f'编号为{self.no}的哲学家放下左边的叉...')
        self.records.put([self.no, 1, 2])

    # 放下右边的叉
    def putRightFork(self):
        print(f'编号为{self.no}的哲学家放下右边的叉...')
        self.records.put([self.no, 2, 2])


if __name__ == "__main__":

    # 定义一个队列用于存放记录
    records = queue.Queue()

    # 定义5个叉子的锁
    lock = [threading.Lock() for i in range(5)]

    # 定义5个哲学家，分配对应的叉
    philosophers = {}
    for i in range(5):
        if i == 0:
            leftKey = 4
            rightKey = 0
        elif i == 4:
            leftKey = 3
            rightKey = 0
        else:
            leftKey = i - 1
            rightKey = i
        philosophers[i] = DiningPhilosopher(
            i, 2, lock[leftKey], lock[rightKey], records)

    # 所有哲学家开始任务
    for i in philosophers:
        philosophers[i].start()

    for i in philosophers:
        philosophers[i].join()

    print('所有哲学家的任务完成')

    # 将队列中的记录放到列表中
    records_list = []

    while not records.empty():
        records_list.append(records.get())

    print(records_list)

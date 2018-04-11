import threading  
import queue  
import time
from odps import ODPS
from odps.df import DataFrame

import pandas as pd



o = ODPS('LTAI9Sv5Havraw43', 'oXKPuuTuWuivpYrj1Ig58KlyYZofp7', 'yxjr_tmp',
     endpoint='http://service.odps.aliyun.com/api')

table_name=input("输入表名：")
lines=input("如有需要请输入行数限定：")
file_path=input("输入文件路径：")
sep=input("输入分隔符：")
p = queue.Queue()

exitFlag = 0

class worker(threading.Thread):  
    def __init__(self,threadID,name,queue):  
        threading.Thread.__init__(self)  
        self.q=queue 
        self.threadID = threadID
        self.name=name
#         self.thread_stop=False
        
    def run(self):
        print("Starting " + self.name)
        process_data(self.name, self.q)
        print("Exiting " + self.name)
                
def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not q.empty():
            sql = q.get()
            print("thread%s running ：%s"%(threadName,sql))
            queueLock.release()
            tmp=o.execute_sql(sql).open_reader()
            p.put([i.values for i in tmp])
        else:
            queueLock.release()

            
st = time.time()
queueLock = threading.Lock()       
q=queue.Queue(5) 

#根据表行数产生sql
if len(lines)==0:
    with o.execute_sql("select sum(1) from "+table_name).open_reader() as reader :
        for record in reader:
            length=record[0]


else:
    length=int(lines)
id=[1]+[i*10000 for i in range(1,int(length/10000)+1,1)]+[length]
k=int(length/10000)+1
sql_tmp=["select * from (select *,row_number() over (partition by 1 order by 1) id  from "+table_name+")a where id>="+str(i)+" and id<"+str(j) for i in id[:-1] for j in id[1:]]

sql=[sql_tmp[i] for i in range(0,k*k,k+1)]

#设置8个线程
threads=[]
cnt=9
if k<9:
    cnt=k

for i in range(cnt):
    pe=worker(i,str(i),q)
    pe.start()
    threads.append(pe)
    
queueLock.acquire()

for i in sql:
    q.put(i)#产生任务消息  

queueLock.release()

while not q.empty():
    pass

exitFlag = 1

print("***************leader:wait for finish!")  
for k in threads:
    k.join()#等待所有任务完成  
print("***************leader:all task finished!")

result=[]
while not p.empty():
    result=result+p.get()
    
    
result=pd.DataFrame(result)
result.columns=list((((o.get_table(table_name)).to_df()).to_pandas()).columns)+['id']

if len(sep)==0:
    sep=','
result.to_csv(file_path,sep=sep)


et = time.time()

ttttt=input("运行完成，共耗时："+str(int(et - st))+"秒,输入任意键结束")
__author__ = 'chi'

from WeiboDataAnalysis.postgres import PostgresConn
import random
import math
import matplotlib.pyplot as plt

def main():
    num_select=500
    db = PostgresConn()
    sql='select uid,fan_num from "user" where verify=True;'
    users = db.query(sql)

    random.shuffle(users)
    select_users=users[:num_select]

    user_id=map(lambda x:x[0],select_users)
    user_fannum=map(lambda x:x[1],select_users)

    fan_num=map(lambda x:math.log(x+1),user_fannum)

    plt.hist(fan_num)
    plt.show()
    print(user_id)
    f=open('user_'+str(num_select)+'.txt','w')
    for id in user_id:
        f.write(id+'\n')
    f.close()

if __name__ == '__main__':
    main()

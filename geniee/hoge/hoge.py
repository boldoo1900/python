import pandas as pd
import matplotlib.pyplot as plt
from fabric import Connection

def task1():
    for i in range(100):
        if i%3 == 0:
            print("Fizz")
        elif i%5 == 0:
            print("Buzz")
        elif i%15 == 0:
            print("FizzBuzz")
        else:
            print(i)

def task2():
    #1 
    a = "パトカー"
    b = "タクシー"
    # a = ("パ","ト","カ", "ー")
    # b = ("タ", "ク", "シ", "ー")

    print(''.join(''.join(x) for x in zip(a,b)))    # string and Tuple both ok

    #2
    strr = 'パタトクカシーー'
    str_1 = slice(1)
    str_3 = slice(2, 3, 1)
    str_5 = slice(4, 5, 1)
    str_7 = slice(6, 7, 1)
    # print(strr[str_1] + strr[str_3] + strr[str_5] + strr[str_7])
    print(strr[::2])

    #3
    print(strr[::-1])

def task3(name, age):
    print("私の名前は"+ name +"です．年齢は"+ age +"歳です．")
    print("私の名前は%sです．年齢は%s歳です．" % (name, age))       # format
    print(f"私の名前は{name}です．年齢は{age}歳です．")             # f-string

def task4():
    x = set(['pa', 'ra', 'pa', 'ra', 'pa', 'ra', 'di', 'se'])
    y = set(['pa', 'ra', 'gr', 'ap', 'h'])

    # 和集合
    print(x.union(y))

    # 積集合
    print(x.intersection(y))

    # 差集合
    print(x.difference(y))

def task5():
    x = input("Enter sentence: ")
    x = x.replace('.', '')
    arr = x.split()

    bb = dict(zip(arr,[arr.count(i) for i in arr ]))
    # {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    cc = sorted(bb.items(), key=lambda x: x[1])
    ll = len(cc)

    # My name is MB. I work in Japan. My Hobby is basketball.
    print(bb)
    print(cc[ll-1] + cc[ll-2] + cc[ll-3])

def task6():
    # dt = pd.read_csv("shop.log", index_col=1, skiprows=1).T.to_dict()
    # pd.read_csv("shop.log")
    # print(dt[0])

    log_data  = open('shop.log', 'r')
    split_list = []

    for line in log_data:
        # items = line.split('\t')
        
        # shop_id = items[0].split(":", maxsplit=1)[1]
        # name = items[1].split(":", maxsplit=1)[1]
        # user_id = items[2].split(":", maxsplit=1)[1]
        # timestamp = items[3].split(":", maxsplit=1)[1]
        # revenue = items[4].split(":", maxsplit=1)[1].rstrip()

        # split_list.append([shop_id, name, user_id, timestamp, revenue])
        split_list.append([item.split(":", maxsplit=1)[1] for item in line.rstrip().split('\t')])       # 78~86 by one line

    df = pd.DataFrame(split_list, columns=['shop_id', 'name', 'user_id', 'timestamp', 'revenue'])
    # print(df)
    return df

def task7_1():
    df = task6()

    # sorting dataframe 
    df.sort_values("shop_id", inplace = True)

    filter = df["shop_id"]=="1"
    df.where(filter, inplace = True) 

    # print(df)
    df.revenue=pd.to_numeric(df.revenue)

    ax = plt.gca()
    df.plot(kind='line',x='timestamp',y='revenue',ax=ax)
    # plt.show()

def task7_2():
    df = task6()

    df["revenue"] = pd.to_numeric(df["revenue"])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    mask = (df['timestamp'] > '2020-04-03') & (df['timestamp'] <= '2020-04-5') & (df["shop_id"] == "1")
    df = df.loc[mask]

    new_df = df.groupby(['name'], sort=True).sum().reset_index()
    new_df = new_df.sort_values(by = ['revenue'], ascending=False)

    print(new_df.head(5))

def task8():
    df = task6()

    df.to_csv (r'test.csv', index = False, header=True)
    
    conn = Connection("fenrir", user='munkhbold-bayasgalan', connect_kwargs={'password': "Passphrase HERE!!!"})
    conn.put('test.csv', remote='/home/local/GENIEE/munkhbold-bayasgalan/')

    print(result)

# task1()
# task2()
# task3("MB", "213")
# task4()
# task5()
# task6()
# task7_1()
# task7_2()
# task8()
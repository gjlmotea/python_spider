# -*- coding: utf-8 -*-
import sys
import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import unicodecsv

current=time.strftime("%Y-%m-%d-%H%M",time.localtime()) #年月日時分
print("Current Time:",current)
filename = ['LOL_銅牌','LOL_銀牌','LOL_黃金','LOL_白金','LOL_鑽石','LOL_全部']#產生6個CSV檔 檔名

try:
    rec_time=str(input('是否依現在時間點來做CSV檔命名(以免覆蓋之前的時間點)? (y/N)'))
except:
    print("發生錯誤")
    raise
else:
    if(rec_time=='y' or rec_time== 'Y'):
        print("(依照時間點進行檔案命名)")
        filename = ['LOL_銅牌'+current,'LOL_銀牌'+current,'LOL_黃金'+current,'LOL_白金'+current,'LOL_鑽石'+current,'LOL_全部'+current]
    else:
        print("(不依時間點進行檔案命名)")

#網站的homepage(index page)排位為黃金
ranking = ['bronze','silver','','platinum','diamond','all']     #網址的一部份
#           銅牌      銀牌  黃金    白金      鑽石      全部



headers = {}
headers['User-Agent'] = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"

rs = requests.session()

for r in range(len(ranking)):
    url = 'https://www.leagueofgraphs.com/zh/champions/builds/'+ranking[r]
    res = rs.get(url, verify=True, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.select(".medium-24 tr")


    with open(filename[r]+'.csv', 'wb') as csvfile:
        writer = unicodecsv.writer(csvfile,encoding='utf-8-sig')
        writer.writerow([u"編號","名字","選用率","勝率","禁用率","擊殺","死亡","助攻","場均五連殺","定位","定位","定位"])


        i=0
        #print("編號\t名字\t\t選用率\t勝率\t禁用率\t擊殺\t死亡\t助攻\t場均五連殺\t定位\t\t定位\t\t定位")


        try:
            for ele in table:       #table中每位英雄的tr
                    i=i+1
                    if(i==16 or i==17 or i==33 or i==49 or i==65 or i==81 or i==97 or i==113 or i==129 or i==145):  #網頁排版斷行
                        continue;
                    tr_soup = BeautifulSoup(table[i].text, 'html.parser')
                    #print(tr_soup)
                    mytext=re.sub(" {1,}", " ", tr_soup.text)    #把多個空白縮減為一個空白
                    mytext=mytext.replace("\n","")
                    mytext=mytext.replace("\r","")

                    sp_pat = re.compile(r' ')      #空白符號作為斷格
                    result = re.split(sp_pat,mytext)
                    #print(result)
                    
                    pct_pat = re.compile(r'%')     #百分比符號作為斷格
                    hero = result[4]
                    pick = re.split(pct_pat,result[-10])
                    win = re.split(pct_pat,result[-9])
                    ban = re.split(pct_pat,result[-8])
                    kill = result[-7]
                    death = result[-5]
                    assist = result[-3]
                    ave5k = result[-2]
                    myspace='\t\t'     #排版用
                    if(len(hero)>=4):
                       myspace='\t'
                    else:
                       myspace='\t\t'
                    role=['','','']
                    if(result[-11]!=''):
                        role[0]=result[-11];
                        role[0]=role[0].replace(",","")
                        if(result[-12]!=''):
                            role[1]=result[-12];
                            role[1]=role[1].replace(",","")     #去除逗號
                            if(result[-13]!=''):
                                role[2]=result[-13];
                                role[2]=role[2].replace(",","")

                    myspace2='\t\t'     #排版用
                    if(len(role[0])>=4):
                       myspace2='\t'
                    else:
                       myspace2='\t\t'                


                    role0 = role[0].encode("utf-8").decode("cp950", "ignore") # for print 簡字編碼問題 'cp950' codec can't encode character '\u8fdc'(远)
                    role1 = role[1].encode("utf-8").decode("cp950", "ignore")
                    role2 = role[2].encode("utf-8").decode("cp950", "ignore")
                    
                    #print(result[1],"\t",hero,myspace,pick[0]+"%\t",win[0]+"%\t",ban[0]+"%\t",kill[0]+"\t",death[0]+"\t",assist[0]+"\t",ave5k,"\t"+role[0]+myspace2+role[1]+"\t"+role[2]+"\t")
                    print("%s\t%s%s%s%%\t%s%%\t%s%%\t%s\t%s\t%s\t%s\t%s%s%s\t%s\t"%(result[1],hero,myspace,pick[0],win[0],ban[0],kill[0],death[0],assist[0],ave5k,role[0],myspace2,role[1],role[2])) #速度較快
                    writer.writerow([result[1],hero,pick[0],win[0],ban[0],kill[0],death[0],assist[0],ave5k,role[0],role[1],role[2]])
            
        except  IndexError as e:    #超過141個英雄範圍之index
            print("---Ranking: ",ranking[r],"End ---")
            time.sleep(0.5)         #for requests.exceptions.ConnectionError
        except Exception as e:
            print(str(e))


rs.close()
print("====== END ======")

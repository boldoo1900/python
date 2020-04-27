from lib2to3.pgen2.grammar import line
import os
import csv
import sys
import urllib.request
from click._compat import raw_input
from flask import json, render_template
import urllib


class Example(object):
    @staticmethod
    def strreverse(val):
        mlist = list(val)
        #mlist.list.reverse()

        mreturn = []
        mlen = len(mlist)
        for idx, row in enumerate(mlist):
            mreturn.append(mlist[mlen-idx-1])
        print(''.join(mreturn))

    @staticmethod
    def testfile(val):      # sample read file and create if not exists

        currentpath = os.path.dirname(os.path.abspath(__file__))        # get current project directory
        #print(currentpath+'\\..\\files\\test.txt');
        val.sort(reverse=True);
        mode = 'a' if os.path.exists(currentpath+'\\..\\files\\test.txt') else 'w'
        with open(currentpath+'\\..\\files\\test.txt', mode) as f:
            #print(', '.join(str(e) for e in val))
            f.write(', '.join(str(e) for e in val))

    @staticmethod
    def testtable():

        mtitle = ''
        mline = ''
        for i in range(1, 10):
            mtitle += ' '+str(i)+'  '
            mline += '----'

        print(mtitle)
        print(mline)
        for i in range(1, 10):
            mtitle = ''
            for j in range(1, 10):
                mtitle += str(i)+'*'+str(j)+' '
            print(mtitle)

    @staticmethod
    def testcsv(postid):
        arr = []
        csv_file = csv.reader(open('D:\\installs\\python\\KEN_ALL_ROME.CSV', "r", encoding="shift-jis"), dialect=csv.excel)
        for row in csv_file:
            if row[0] == postid:
                print(row)
                arr = row

        return render_template('posttest.html', val=arr)

    @staticmethod
    def getaddressbypostalcode():
        number = raw_input('Enter porstal code:\n')

        mUrl = "http://zip.ricollab.jp/{0}.json".format(number)
        with urllib.request.urlopen(mUrl) as url:
            data = json.loads(url.read().decode("utf-8"))
            print(data['zipcode'])
            print('prefecture:'+data['address']['prefecture'])
            print('city:      '+data['address']['city'])
            print('town:      '+data['address']['town'])
            print('Address:   '+data['address']['prefecture']+', '+data['address']['city']+', '+data['address']['town'])
            print('Address(yomi): '+data['yomi']['prefecture']+', '+data['yomi']['city']+', '+data['yomi']['town'])
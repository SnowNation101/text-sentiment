# -*- coding: utf-8 -*-
# @Time    : 19-3-28 上午10:56
# @Author  : Redtree
# @File    : main.py
# @Desc :

import emotion_cn

if __name__ == '__main__':
    # wb=openpyxl.load_workbook("./input.xlsx")
    # table = wb['Sheet1']
    # #print(wb.sheetnames)
    # table['F1'] = 'score'
    # len = table.max_row
    # for i in range(2,len+1):
    #     input_text = table['E'+str(i)].value
    #     out_put = emotion_cn.getMoodValue(input_text)
    #     table['F'+str(i)] = out_put
    #     print(i)
    # wb.save("./output.xlsx")


    # while 1>0 :
    #     lg = input("switch language,type 'CN' or 'ENG' ,if you want to exit ,type '0' "+'\n')
    #     if lg == 'CN':
    #         print("type chinese text to get result,if you want to exit ,type '0' ")
    #         while 1 > 0:
            while 1 > 0:
                input_text = input('\n')
                out_put = emotion_cn.getMoodValue(input_text)
                print(out_put)
    #             if input_text == '0':
    #                 break
    #     elif lg == 'ENG':
    #         print("type english text to get result,if you want to exit ,type '0' ")
    #         while 1 > 0:
    #             input_text = input('\n')
    #             out_put = emotion_eng.getMoodValue(input_text)
    #             print(out_put)
    #             if input_text == '0':
    #                 break
    #     elif lg =='0':
    #         break


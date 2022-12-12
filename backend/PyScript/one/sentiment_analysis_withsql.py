# coding: utf-8
import jieba
import pymysql
import os

# 创建连接MYSQL的类
class TestMysql:
    # 初始化变量
    def __init__(self, username, host, passwd, database):
        self.username = username
        self.host = host
        self.passwd = passwd
        self.database = database

    # 创建数据库连接
    def conn_mysql(self):
        conn = pymysql.connect(user=self.username, host=self.host, password=self.passwd, db=self.database)
        return conn

    # 关闭数据库的提示信息
    def close_mysql(self):
        # print("MySQL is Closed")
        pass

    # 查询数据
    def get_data(self,sql):
        self.conn = self.conn_mysql()
        cur = self.conn.cursor()

        # while True:
        #sql = input('输入SQL语句:') #通过这里进行链接
        #print('Received Message: ', sql)  # 这里发过来的data需要是sql语言，直接用于操作数据库
        cur.execute(sql)
        self.conn.commit()
        results = cur.fetchall()
        # if len(results) != 0:
        #     print('Returned Data:')
        #     for i in results:
        #         print(str(i))
        # yn = input('按N断开连接,任意键继续：').strip()
        # if yn == 'N':
        #     break

        cur.close()
        self.close_mysql()
        return results

class Struct(object):
    def __init__(self, word, sentiment, pos, value, class_value):
        self.word = word
        self.sentiment = sentiment
        self.pos = pos
        self.value = value
        self.class_value = class_value


class Result(object):
    def __init__(self, score, score_words, not_word, degree_word):
        self.score = score
        self.score_words = score_words
        self.not_word = not_word
        self.degree_word = degree_word


class Score(object):
    # 七个情感大类对应的小类简称:
    score_class = {'乐': ['PA', 'PE'],
                   '好': ['PD', 'PH', 'PG', 'PB', 'PK'],
                   '怒': ['NA'],
                   '哀': ['NB', 'NJ', 'NH', 'PF'],
                   '惧': ['NI', 'NC', 'NG'],
                   '恶': ['NE', 'ND', 'NN', 'NK', 'NL'],
                   '惊': ['PC']
                   }
    # 大连理工大学 -> ICTPOS 3.0
    POS_MAP = {
        'noun': 'n',
        'verb': 'v',
        'adj': 'a',
        'adv': 'd',
        'nw': 'al',  # 网络用语
        'idiom': 'al',
        'prep': 'p',
    }

    # 否定词
    NOT_DICT = set(['不', '不是', '不大', '没', '无', '非', '莫', '弗', '毋',
                    '勿', '未', '否', '别', '無', '休'])

    def __init__(self, sentiment_dict_path, degree_dict_path):
        #读取情感词汇词典
        self.sentiment_struct, self.sentiment_dict = self.load_sentiment_dict(sentiment_dict_path)
        #读取程度词词典
        self.degree_dict = self.load_degree_dict(degree_dict_path)

    def load_degree_dict(self, dict_path):
        #读取程度词词典，{word:degre}形式
        degree_dict = {}
        with open(dict_path, 'r', encoding='UTF-8') as f:
            for line in f:
                line = line.strip()
                word, degree = line.split('\t')
                degree = float(degree)
                degree_dict[word] = degree
        return degree_dict #返回字典类型

    def load_sentiment_dict(self, dict_path):
        #读取情感词词典，返回的是 对于每一个词典，记录其词语、情绪、位置、极性、强度的结构
        sentiment_dict = {}
        sentiment_struct = []
        with open(dict_path, 'r', encoding='UTF-8') as f:
            for index, line in enumerate(f):
                if index == 0:  # 第一行是标题，跳过
                    continue
                items = line.split('\t')
                word = items[0] #词典里的词
                pos = items[1] #词性种类
                sentiment = items[4] #情绪分类
                intensity = items[5]  # 强度1, 3, 5, 7, 9五档, 9表示强度最大, 1为强度最小.
                polar = items[6]  # 极性

                # 将词性转为 ICTPOS 词性体系
                pos = self.__class__.POS_MAP[pos]
                intensity = int(intensity)
                polar = int(polar)

                #根据极性转化一下表达方式(0,1,2) -> (-1,0,1)
                value = None
                if polar == 0:  # neutral
                    value = 0
                elif polar == 1:  # positive
                    value = intensity
                elif polar == 2:  # negtive
                    value = -1 * intensity
                else:  # invalid
                    continue

                key = word #词汇
                sentiment_dict[key] = value

                # 找对应的情绪类
                for item in self.score_class.items():
                    key = item[0]
                    values = item[1]
                    for x in values:
                        if (sentiment == x):
                            class_value = key

                #对于每一个词典，记录其词语、情绪、位置、极性、强度
                sentiment_struct.append(Struct(word, sentiment, pos, value, class_value))
        return sentiment_struct, sentiment_dict

    def classify_words(self, words):  #对分词后的评论，划分一下情感词、程度词和否定词
        # 这3个键是词的序号
        sen_word = {}
        not_word = {}
        degree_word = {}
        # 找到对应的sentiment, not, degree;
        for index, word in enumerate(words):#words是分词后的列表
            if word in self.sentiment_dict and word not in self.__class__.NOT_DICT:
                sen_word[index] = self.sentiment_dict[word]
            elif word in self.__class__.NOT_DICT and word not in self.degree_dict:
                not_word[index] = -1
            elif word in self.degree_dict:
                degree_word[index] = self.degree_dict[word]
        return sen_word, not_word, degree_word

    def get2score_position(self, words): #通过判断情感词与程度词、否定词的位置关系，得到最终的情感score
        # 对分词后的评论，找到情感词、程度词和否定词
        sen_word, not_word, degree_word = self.classify_words(words)

        score = 0
        start = 0
        # 找到情感词、程度词和否定词位置
        sen_locs = sen_word.keys()
        not_locs = not_word.keys()
        degree_locs = degree_word.keys()
        senloc = -1
        for i in range(0, len(words)): #下标访问分词列表
            if i in sen_locs: #如果是情感词
                W = 1  # 情感词间权重重置
                not_locs_index = 0
                degree_locs_index = 0

                senloc += 1 #情感词列表sen_locs中的下标

                # start用于记录这个词前面那个情感词的位置
                if (senloc == 0):
                    start = 0
                elif senloc < len(sen_locs):
                    start = previous_sen_locs

                #遍历上一个情感词和这一个情感词之间的词语，判断有没有否定词和程度词
                for j in range(start, i):  # 词间的相对位置
                    # 如果有否定词，记录位置并*-1
                    if j in not_locs:
                        W *= -1
                        not_locs_index = j
                    # 如果有程度副词，记录位置并*degree
                    elif j in degree_locs:
                        W *= degree_word[j]
                        degree_locs_index = j

                # 判断否定词和程度词的位置：1）否定词在前，程度词减半(加上正值)；不是很   2）否定词在后，程度增强（不变），很不是
                if ((not_locs_index > 0) and (degree_locs_index > 0)):
                    if (not_locs_index < degree_locs_index):
                        degree_reduce = (float(degree_word[degree_locs_index] / 2))
                        W += degree_reduce
                        # print (W)

                #print(W,float(sen_word[i]))
                score += W * float(sen_word[i])  # 直接添加该情感词分数
                previous_sen_locs = i
        return score


if __name__ == '__main__':
    # 定义变量
    username = 'root'
    host = '127.0.0.1'
    passwd = '123456'
    database = 'text_sentiment'

    # 使用try--except
    try:
        # 创建TestMysql的实例
        mysql = TestMysql(username, host, passwd, database)
        mysql.conn_mysql()
        # sql = ""
        # mysql.get_data(sql)
    except pymysql.err.ProgrammingError as e:
        print("Exception Error is %s" % (e))
    except pymysql.err.OperationalError as e:
        print("Exception Error is %s" % (e))

    print(os.getcwd())
    sentiment_dict_path = "./PyScript/one/sentiment_words_chinese.tsv" #大连理工大学中文情感词汇词库
    degree_dict_path = "./PyScript/one/degree_dict.txt" #程度词

    # 文件读取
    # data = pd.read_excel('../source/dataset1.xlsx')
    sql = "select text from tmp where id = 1;"
    #data = input('input test sentence:')
    print(sql)
    data = mysql.get_data(sql)
    data = data[0][0]

    # 识别情感词典和程度词典
    score = Score(sentiment_dict_path, degree_dict_path)

    tlist = []
    words = [x for x in jieba.cut(data)]  # 分词
    print(words)
    # 判断情感词与程度词、否定词的相对位子，并计算分数
    result1 = score.get2score_position(words)
    id=1
    tlist.append(id)
    #tlist.append(words)
    tlist.append(str(result1))
    print(str(result1))

    sql = "update tmp set value = " + str(result1) + " where id = 1;"
    print(sql)
    mysql.get_data(sql)
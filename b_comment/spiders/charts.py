# coding:utf-8
# 导入csv库
import csv
from wordcloud import WordCloud
from pyecharts.charts import Bar
import jieba
from aip import AipNlp
import collections # 词频统计库
from pyecharts import options as opts
import time

def Configuration():
    wcd = WordCloud(
        # 字体路径
        font_path='/Library/Fonts/Songti.ttc',
        # 背景图片设置
        background_color='white',
        # 单词是否重复展示
        repeat=True,
        # 画布边缘留白的空隙
        margin=2,
        # 最多显示词量
        max_words=1000,
        # 图片宽度
        width=1000,
        # # 图片高度
        height=980,
        # 清晰度
        scale=5,
        # 最大字体大小
        max_font_size=80,
        # 最小字体大小
        min_font_size=10,
        # 颜色组
        colormap="tab20c")
    return wcd


def Cloud(wcd):
    # 导入停用表，生成列表
    stwlist = [line.strip() for line in open('stop.txt', encoding='utf-8').readlines()]

    # 词频字典
    word_ = {}

    with open('yzsy.csv', 'r', encoding='utf-8')as f:
        content_list = []
        rows = csv.reader(f)
        for r in rows:
            r[0] = r[0].replace('\n', '') if '\n' in r[0] else r[0]
            # 循环取出列表的第一列评论，添加至列表
            content_list.append(r[0])
        # 将列表的数据拼接在一起，形成长串字符串
        split_list = ''.join(content_list).split(',')
        # 将字符串进行中文分词
        words = jieba.cut(split_list[0], cut_all=False, HMM=True)

        for word in words:
            # 筛选掉与停词表相符的分词
            if word.strip() not in stwlist:
                # 筛选分词小于1个的
                if len(word) > 1:
                    # 筛选掉换行
                    if word != '\t':
                        if word != '\r\n':
                            # 计算词频
                            if word in word_:
                                word_[word] += 1
                            else:
                                word_[word] = 1
        # 将词汇和词频以字典的形式保存
        word_freq = {}
        for word, freq in word_.items():
            word_freq[word] = freq
        # 将词频字典填入词云图
        wcd.generate_from_frequencies(word_freq)
        wcd.to_image()
        wcd.to_file("b_clod.png")
        print('词云图生成成功！')


def Py_bar():
    with open('yzsy.csv', 'r', encoding='utf-8')as f:
        rows = csv.reader(f)
        time_list = []
        for row in rows:
            if len(row[1].split(' ')) == 2:
                # 将评论的小时进行提取
                time = row[1].split(' ')[1].split(':')[0]
                time_list.append(time)
        # 对时间段中的小时进行词频统计
        word_counts = collections.Counter(time_list)
        word_freq = []
        for word, freq in word_counts.items():
            word_freq.append((word, freq))
        # 进行降序排列
        word_freq.sort(key=lambda x: x[1], reverse=True)
        time = []
        count = []
        # # 查看前200个结果
        for i in range(24):
            word, freq = word_freq[i]
            time.append(word)
            count.append(freq)

        bar = (
            Bar()
                .add_xaxis(time)
                .add_yaxis("时间段", count)
                .set_global_opts(title_opts=opts.TitleOpts(title="《豫章书院》视频评论时段统计"))
        )
        bar.render('评论时间段分析.html')
    print('评论时间段分析完毕！')

def Emotion():
    csvFile = open("newjob.csv", 'w', newline='')  # 创建文件
    writer = csv.writer(csvFile)
    writer.writerow(('评论', '正向指数', '负向指数', '情感分类'))  # 设置表头

    # 配置百度接口
    APP_ID ='16802343'
    API_KEY = 'DWHSIPtzUxP9IRj5F93xIzGS'
    SECRET_KEY = 'I4vrC0x42looiNl1KCSL64HAv5uWt1A5'
    # 配置账号，密码等
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    count = 0
    with open('yzsy.csv', 'r', encoding='utf-8')as f:
        rows = csv.reader(f)
        for r in rows:
            text = r[0].replace('\n', '') if '\n' in r[0] else r[0]
            try:
                # 将数据放到百度中解析
                content = client.sentimentClassify(text)

                text = content["text"], #获取分析的文本
                positive = str(round(content["items"][0]['positive_prob'] * 100,3)) + "%", #获取正向情感
                negative = str(round(content["items"][0]['negative_prob'] * 100,3))+ "%",#获取负向情感
                type_num = content["items"][0]['sentiment'], #获取情感分析
                if type_num == '2':
                    type = '正向'
                elif type_num == '1':
                    type = '中性'
                else:
                    type ='负向'
                writer.writerow((text,positive,negative,type))
                count += 1
                print('已分析{}条数据'.format(count))
                time.sleep(2)
            except:
                continue
        print('情感分析完毕！')



if __name__ == '__main__':

    # # 生成词云图的函数
    # Cloud(Configuration())
    # # 时间段统计函数
    # Py_bar()
    Emotion()

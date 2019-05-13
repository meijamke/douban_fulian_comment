"""
    日期：2019.5.13
    作者：meijamke
    功能：爬取豆瓣复仇者联盟的前20万短评，将关键词的词频结果保存为csv

    补充：词云图制作 https://wordart.com/create

    列表的
    append：往列表添加一个元素，这个元素可以是一个列表，但将作为内嵌列表加入。
    extend：合并两个列表
    +：     合并两个列表
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
# 忽略警告
import warnings

warnings.filterwarnings('ignore')

# 解决中文和负数显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# 获取一个网页的评论内容：
# 评论人、评分、评论时间、有用数量、评论内容
def get_data(url):
    try:
        r = requests.get(url=url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        info_list = soup.find_all('div', class_="comment-item")
        data_list = []
        for line in info_list:
            dic = {'评论人': line.find('span', class_="comment-info").find('a').text,
                   '评分': int(line.find('span', class_="comment-info").find_all('span')[1]['class'][0][-2:]),
                   '评论时间': line.find('span', class_="comment-time").text.replace('\n', '').replace(' ', ''),
                   '有用数量': int(line.find('span', class_="votes").text),
                   '评论内容': line.find('span', class_="short").text.replace('\n', '')}
            data_list.append(dic)
        return data_list
    except:
        return []


# 获取n个网页的url
def get_url(n):
    url_list = []
    for i in range(n):
        url_list.append(
            "https://movie.douban.com/subject/26100958/comments?start={}&limit=20&sort=new_score&status=P".format(
                i * 20))
    return url_list


# 统计词频
def word_count(word, str_):
    n = 0
    for i in str_:
        if word in i:
            n += 1
        else:
            continue
    return n


def main():
    data_list = []
    n = 1
    url_list = get_url(50)
    for url in url_list:
        data_list.extend(get_data(url))
        print('成功获取{}条数据'.format(n * 20))
        n += 1
    print(data_list)
    print(len(data_list))
    # 数据格式转换：字典——>表格
    df = pd.DataFrame(data_list)
    # 评论字数数据分布
    df['评论字数'] = df['评论内容'].str.len()
    plt.figure(figsize=(12, 5))
    plt.title('评论字数分布')
    df['评论字数'].hist(bins=20, edgecolor='white')
    plt.grid(linestyle='--')
    plt.show()
    # 有用数量<2000数据分布
    plt.figure(figsize=(12, 5))
    plt.title('有用数量<2000数据分布')
    df[df['有用数量'] < 2000]['有用数量'].hist(bins=50, edgecolor='white')
    plt.grid(linestyle='--')
    plt.show()
    # 评论字数与有用数量的关系
    plt.figure(figsize=(12, 5))
    plt.title('评论字数与有用数量的关系')
    plt.scatter(df['评论字数'], df['有用数量'], alpha=0.4)
    plt.xlabel('评论字数')
    plt.ylabel('有用数量')
    plt.grid(linestyle='--')
    plt.show()
    # 评论字数与评分关系
    plt.figure(figsize=(12, 5))
    plt.title('评论字数与评分关系')
    plt.scatter(df['评论字数'], df['评分'], alpha=0.4)
    plt.xlabel('评论字数')
    plt.ylabel('评分')
    plt.grid(linestyle='--')
    plt.show()
    # 评论时间与有用数量关系
    plt.figure(figsize=(12, 5))
    plt.title('评论时间与有用数量关系')
    plt.scatter(df['评论时间'], df['有用数量'], alpha=0.4)
    plt.xlabel('评论时间')
    plt.ylabel('有用数量')
    plt.grid(linestyle='--')
    plt.show()
    # 评论时间与评分关系
    plt.figure(figsize=(12, 5))
    plt.title('评论时间与有用数量关系')
    plt.scatter(df['评论时间'], df['评分'], alpha=0.4)
    plt.xlabel('评论时间')
    plt.ylabel('评分')
    plt.grid(linestyle='--')
    plt.show()

    # 关键人物分析
    # 计算不同关键词出现的频率
    name_list = ['美队', '钢铁侠', '灭霸', '黑寡妇', '雷神', '浩克', '惊奇队长',
                 '鹰眼', '蚁人', '奇异博士', '蜘蛛侠', '星云', '黑豹']
    lst = []
    for name_ in name_list:
        lst.append({'关键词': name_, '出现频率': word_count(name_, df['评论内容'])})
    # 结果保存为CSV
    name_freq = pd.DataFrame(lst)
    name_freq.to_csv('name_freq.csv')


if __name__ == '__main__':
    main()

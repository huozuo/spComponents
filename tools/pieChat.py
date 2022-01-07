'''
画饼状图
'''

from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.render import make_snapshot
from pyecharts.charts import Grid
from snapshot_phantomjs import snapshot
import threading



def getPie(data,name):
    '''
    style like this https://gallery.pyecharts.org/#/Pie/pie_radius
    样式为 空心 的圆环
    :param data: 字典
    :param name: title
    :return:
    '''
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(data.keys(), data.values())],
            radius=["45%", "75%"],
            center=["50%", "56%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=name, pos_top="13",pos_left="1%"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="25%", pos_left="8%"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="size{b}: {d}%"))

        # .render("pie_radius.html")
    )
    return c


def getPie1(data,name):
    '''
    style like this https://gallery.pyecharts.org/#/Pie/pie_radius
    样式为 空心 的圆环
    :param data:
    :param name:
    :return:
    '''
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(data.keys(), data.values())],

            center=["50%", "56%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=name, pos_top="13",pos_left="1%"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="25%", pos_left="8%"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="size{b}: {d}%"))

        # .render("pie_radius.html")
    )
    return c

def getDatafromTxt(filename):
    with open(filename) as f:
        data = f.readline().strip('\n')
        count  = 0
        name = ""
        dic = ""
        while(data!=''):
            if count == 0:
                name = data
            else:
                dic = data
                yield name,eval(dic) # eval将字符串转换成dict

            count =  (count+1)%2
            data = f.readline().strip('\n')







def plotPie(name, data):
    # print(name)
    # print(dic)
    make_snapshot(snapshot, getPie(data,name).render(), name+".pdf")
    # make_snapshot(snapshot, getPie1(data, name).render(), name + "without-20.pdf")
    # getGraph(data, name).render("pie_radius.html")
    print("######"+name+"  :绘制完毕######")


if __name__=="__main__":
    # data = {20: 924, 6: 134, 4: 60, 17: 11, 3: 8, 8: 1}
    # name = "ApplePullFortnite_retweet_net"
    # getPie(data, name).render("pie_radius.html")

    fileName = "E:\\教研室\\论文\\匹配表征实验数据\\原子规模分布数据.txt"
    print("$$$$开始绘制$$$$$")
    for name,dic in getDatafromTxt(fileName):
        # del dic[20] #去掉size为20
        plotPie(name,dic)

    print("$$$$$$All is done$$$$$$")



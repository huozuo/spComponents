
'''
画直方图
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



def getBar(name,xaxis,data1,data2):
    '''
    画两个数据的对比直方图
    :param name:
    :param xaxis:
    :param data1:
    :param data2:
    :return:
    '''
    c = (
        Bar({"theme": ThemeType.MACARONS})
        #{"theme": ThemeType.MACARONS},
        #init_opts=opts.InitOpts(width="2000px",height="600px")
            .add_xaxis(xaxis)
            .add_yaxis("浮点矩阵分解", data1)
            .add_yaxis("布尔矩阵分解", data2,category_gap=15)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"interval":"0","rotate":-45}),
            # title_opts=opts.TitleOpts(title="Bar-旋转X轴标签", subtitle="解决标签名字过长的问题"),
            title_opts=opts.TitleOpts(title=name,pos_top="2%",pos_left="5%"),
            # yaxis_opts=opts.AxisOpts(axislabel_opts={"pos_top":"5"}),
        )
    )
    grid = Grid()
    grid.add(c, grid_opts=opts.GridOpts(width="750px",height="450px", is_contain_label=True))

    return grid

def getSingleBar(name,yName,xaxis,yaxis):
    c = (
        Bar({"theme": ThemeType.MACARONS})
            # {"theme": ThemeType.MACARONS},
            # init_opts=opts.InitOpts(width="2000px",height="600px")
            .add_xaxis(xaxis)
            # .add_yaxis("proportion of star atoms", data, category_gap=25)
            .add_yaxis(yName, yaxis, category_gap=8)
            # .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            # xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": "0", "rotate": -45}),
            xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": "0"}),
            # title_opts=opts.TitleOpts(title="Bar-旋转X轴标签", subtitle="解决标签名字过长的问题"),
            title_opts=opts.TitleOpts(title=name, pos_top="2%", pos_left="5%"),
            # yaxis_opts=opts.AxisOpts(axislabel_opts={"pos_top":"5"}),
        )
    )
    grid = Grid()
    grid.add(c, grid_opts=opts.GridOpts(width="800px", height="400px", is_contain_label=True))
    return grid

def plotBar(xaxis,data1,data2,name):
    getBar(name,xaxis,data1,data2).render("bar-test.html")
    make_snapshot(snapshot, getBar(name,xaxis,data1,data2).render(), name + ".pdf")

def plotSingleBar(name,yName,xaxis,yaxis):

    make_snapshot(snapshot, getSingleBar(name,yName,xaxis,yaxis).render(), name + ".pdf")





if __name__=="__main__":
    # name = "slice error"
    # yName = "err"
    # xaxis = ["wn18_1308","wn18_18301","wn18_21783","wn18_21858","wn18_22085","wn18_25891","wn18_27772","wn18_30579","wn18_34114","wn18_8204"]
    # yaxis = [0.00079,0.00120,0.00057,0.00096,0.00080,
    #          0.00296,0.00051,0.00274,0.00252,0.00124]
    # plotSingleBar(name,yName,xaxis,yaxis)
    # print("done")
    name = "star error"
    yName = "err"
    xaxis = ["wn18_1308","wn18_18301","wn18_21783","wn18_21858","wn18_22085","wn18_25891","wn18_27772","wn18_30579","wn18_34114","wn18_8204"]
    yaxis = [0.03875,0.01968,0.05498,0.02666,0.03946,
             0.03407,0.03836,0.02512,0.01314,0.02671]
    plotSingleBar(name,yName,xaxis,yaxis)
    print("done")
    # filename1 = "E:\\教研室\\论文\\匹配表征实验数据\\初始稀疏表征结果.csv"
    # filename2 = "E:\\教研室\\论文\\匹配表征实验数据\\匹配表征重构网络数据.csv"
    # # names = ["节点数","边数","平均度","直径","平均路径长度","原子总数"]
    # names = ["原子总数"]
    # for name in names:
    #     print("#####"+name+"#####")
    #     print("开始获取数据")
    #     data1 = getListFromCSV.getListFromCSV(filename1,name)
    #     data2 = getListFromCSV.getListFromCSV(filename2,name)
    #     print("开始绘制")
    #     plotBar(data1,data2,name)
    #
    # print("#####画好了#####")

    ###画单个的星型原子占比
    # name = "星型原子占比"
    # data = getListFromCSV.getListFromCSV(filename1,name)
    # plotBar1(data,name)
    # plotBar2()

    # name = "原子真实覆盖率"
    # data1 = [0.10,0.09,0.11,0.17,0.07,0.07,0.09,0.22]
    # data2 = [0.97,0.97,0.95,0.99,1.0,1.0,1.0,0.94]
    # xaxis = ["ca-AstroPh2","com-amazon2","com-dblp2","ntp-ChicagoRegional","opsahl-powergrid","roadNet-CA2","subelj_euroroad_euroroad","wordnet-words2"]
    # plotBar(xaxis,data1,data2,name)
    # print("done")

    # name = "稀疏表征误差"
    # data1 = [0.112, 0.09, 0.132, 0.003, 0.215, 0.156, 0.109, 0.119]
    # data2 = [0.036, 0.036, 0.029, 0.001, 0.032, 0.005, 0.005, 0.031]
    # xaxis = ["ca-AstroPh2", "com-amazon2", "com-dblp2", "ntp-ChicagoRegional", "opsahl-powergrid", "roadNet-CA2",
    #          "subelj_euroroad_euroroad", "wordnet-words2"]
    # plotBar(xaxis, data1, data2, name)
    # print("done")

    # name = "原子数"
    # data1 = [198, 200, 198, 32, 197, 200, 195, 197]
    # data2 = [49, 41, 28, 12, 32, 27, 16, 50]
    # xaxis = ["ca-AstroPh2", "com-amazon2", "com-dblp2", "ntp-ChicagoRegional", "opsahl-powergrid", "roadNet-CA2",
    #          "subelj_euroroad_euroroad", "wordnet-words2"]
    # plotBar(xaxis, data1, data2, name)
    # print("done")

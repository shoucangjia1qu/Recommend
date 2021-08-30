# -*- coding: utf-8 -*-
"""
Created on Tue Jun  17 09:20:29 2021

@author: AoDaDou
"""

import sys
# sys.path.append("D:\mywork\python\Recommend")

from base import Container
from runjob import loadingData, combineRecommend, savingData
import engine as eg
import utils as ut
import warnings

warnings.filterwarnings('ignore')

# 物品近邻数量
K = 5
# 物品总数量
item_nums = 154
# 协同过滤推荐数量
itemcf_nums = 5
# 流行度推荐数量
popular_nums = 5
# lfm推荐数量
lfm_nums = 5


def main(train_path, res_path, test_path=""):
    # train = loadingData(train_path, 'tdid', 'cha_yan_jiu', 'hwzb', dropRows=0)
    train = loadingData(train_path, 'aid', 'cha_yan_jiu', 'hwzb', dropRows=None)
    print(">>>数据导入成功！")
    # 0 数据转换
    couponContainer = Container(ut.datachange, train.to_numpy())
    print(">>>数据转换成功！")


    # 1 推荐训练
    # 1.1 协同过滤引擎
    itemcf = eg.ItemCF()
    itemcf.fit(couponContainer.Item_Users, couponContainer.Item_vectors)
    print(">>>协同过滤训练成功！")
    itemcfRecommend = itemcf.recommend(itemcf_nums, K, couponContainer.User_Items)
    print(">>>协同过滤推荐成功！")


    # 1.2 用户流行度推荐引擎
    favor = eg.FavoriteRecommend()
    favorRecommend = favor.recommend(popular_nums, couponContainer.User_Items)
    print(">>>用户流行度推荐成功！")


    # 1.3 LFM推荐引擎，学习率，隐分子数量，迭代次数，负/正样本比，L2系数
    lfm = eg.LFMRecommend(0.01, 30, 5, 2, 0.01)
    lfm.fit(couponContainer.User_Items, couponContainer.Item_times)
    print(">>>LFM训练成功！")
    lfmRecommend = lfm.recommend(lfm_nums, couponContainer.User_Items)
    print(">>>LFM推荐成功！")


    # 2 整合推荐结果
    res = combineRecommend(list(itemcfRecommend.keys()), itemcfRecommend, favorRecommend, lfmRecommend, blackList=[])
    print(">>>推荐结果整合成功！")
    return res



if __name__ == '__main__':
    print("******************************************")
    print("***              开始运行              ***")
    print("******************************************")
    # 调试时自己输路径
    train_path = 'D:/mywork/python/recommend/dataSet/data_202103.csv'
    res_path = 'D:/mywork/python/recommend/result'
    test_path = 'D:/mywork/python/recommend/dataSet/data_202104.csv'

    # 执行时输入输出目录作为参数
    # train_path = sys.argv[1]
    # print(f"训练集路径：{train_path}")
    # res_path = sys.argv[2]
    # print(f"结果路径：{res_path}")
    # test_path = sys.argv[3]
    # print(f"测试集路径：{test_path}")

    # 1. 训练
    print(">>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>开始训练。。。")
    res = main(train_path, res_path, test_path)
    print(">>>训练结束！\n")

    # 2. 评价
    if test_path != "":
        print(">>>>>>>>>>>>>>>>>>>>>>>>>")
        print("开始评价。。。")
        test = loadingData(test_path, 'aid', 'cha_yan_jiu', 'hwzb', dropRows=0)
        print(">>>测试集数据导入成功！")
        # ut.evaluate(lfmRecommend, test, item_nums)
        ut.evaluate(res, test, item_nums)
        print(">>>评价完成！\n")

    # 3. 保存
    print(">>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>开始保存。。。")
    savingData(res_path, res)
    print(">>>保存结束！")




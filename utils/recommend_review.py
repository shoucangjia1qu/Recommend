# -*- coding: utf-8 -*-
"""
Created on Tue Jun  17 20:43:29 2021

@author: AoDaDou
"""

import numpy as np


# 单个客户推荐的的测评
def singleevaluate(recommendItems, testItems, hit=0, populardict={}):
    """
    计算单个客户推荐的命中数

    Parameters
    ----------
    recommendItems : List
        单个用户推荐的物品列表.
    testItems : Array
        单个用户测试集中的物品数组.
    hit : Int, optional
        初始命中数量，计算单个客户时就是0，多个客户累加会将之前的hit代入. The default is 0.
    populardict : Dict, optional
        累加推荐物品推荐次数的字典. The default is {}.

    Returns
    -------
    hit : Int
        命中数量.
    populardict : Dict
        记录推荐物品-次数的字典.

    """
    for item in recommendItems:
        if item.id in testItems:
            hit += 1
        if item.id not in populardict.keys():
            populardict[item.id] = 0
        populardict[item.id] += 1
    return hit, populardict


# 获取用户测试集的数据
def get_testitems(testItems, user):
    """
    获取单个客户在测试集中的物品数组

    Parameters
    ----------
    testItems : DataFrame
        测试数据.
    user : String
        用户id.

    Returns
    -------
    test_array : Array
        测试集中的数组.

    """
    test_items = testItems[testItems['user']==user]['item']
    return test_items.values


# 推荐系统的测评
def evaluate(recommendItems, testItems, item_nums):
    """
    推荐的评价指标展示，包括hit(命中数量)，precision(查准率)，recall(查全率)，
    cover(覆盖率)，popular(流行度)等指标。
    
    Parameters
    ----------
    recommendItems : Dict
        用户——推荐物品字典
    testItems : DataFrame
        测试集
    item_nums : Int
        物品数量
    """
    # 初始化推荐物品的数量、推荐命中数量、推荐物品的流行度字典
    recommend_nums = 0
    hit = 0
    populardict = {}
    # 求测试集的记录数量、物品数量
    test_nums = 0
    # 遍历求得整体的推荐物品的数量、推荐命中数量、推荐流行度
    n = 0
    for u, cmd_items in recommendItems.items():
        n += 1
        if n%1000 == 0:
            print(f'第{n}个客户，', '累计命中: ', hit)
        test_items = get_testitems(testItems, u)
        if test_items.__len__() == 0:
            continue
        recommend_nums += cmd_items.__len__()
        hit, populardict = singleevaluate(cmd_items,  test_items, hit, populardict)
        test_nums += len(test_items)
    # 求评价指标
    popularArr = np.log(np.array(list(populardict.values()))+1)
    precision = hit*1.0/recommend_nums
    recall = hit*1.0/test_nums
    cover = populardict.__len__()*1.0/item_nums
    popular = sum(popularArr)/populardict.__len__()
    print("hit : %d"%hit)
    print("Precision : %.3f\nRecall : %.3f\nCover : %.3f\nPopular : %.3f\n"%(precision, recall, cover, popular))
    return 





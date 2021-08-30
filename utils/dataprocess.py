# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 09:24:47 2021

@author: ecupl
"""


#__all__ = ['datachange']

# 初始数据转换成需要的数据格式进行保存
def datachange(trainSet):
    """
    数据转换函数，变成模型需要用的数据类型。   

    Parameters
    ----------
    trainSet : Array
        numpy密集矩阵[uesr, item, rat].

    Returns
    -------
    Item_Users : Dict
        物品-用户-分数矩阵.
    Item_times : Dict
        物品喜欢人数.
    Item_vectors : Dict
        物品向量矩阵.
    User_Items : Dict
        用户-物品-分数矩阵.

    """
    # 统计每个物品出现的次数
    Item_times = dict()
    # 统计物品-用户矩阵
    Item_Users = dict()
    # 物品-向量
    Item_vectors = dict()
    # 统计用户-物品矩阵
    User_Items = dict()
    for user, item, rat in trainSet:
        if item not in Item_times.keys():
            Item_times[item] = 0
            Item_Users[item] = dict()
            Item_vectors[item] = []
        if user not in User_Items.keys():
            User_Items[user] = dict()
        # 次数加一
        Item_times[item] += 1
        # 加上用户对应分数
        Item_Users[item][user] = rat
        # 加上分数作为向量
        Item_vectors[item].append(rat)
        # 加上用户的对应物品
        User_Items[user][item] = rat
    return Item_Users, Item_times, Item_vectors, User_Items


# 排序——快速排序
def quickSort(array, key=None, reverse=False):
    # 将输入转成列表
    if not isinstance(array, list):
        array = list(array)
    # 只有单个元素，返回该列表
    if len(array) <= 1:
        return array
    left = []; right = []
    # 开始遍历，拆分左右子集
    if key is None:
        for i in array[1:]:
            if i <= array[0]:
                left.append(i)
            else:
                right.append(i)
    else:
        for i in array[1:]:
            if key(i) <= key(array[0]):
                left.append(i)
            else:
                right.append(i)
    # 递归返回排序顺序
    if reverse:
        return quickSort(right, key=key, reverse=reverse)+ [array[0]]+ quickSort(left, key=key, reverse=reverse)
    else:
        return quickSort(left, key=key)+ [array[0]]+ quickSort(right, key=key)


        


        
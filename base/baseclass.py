# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 09:08:29 2021

@author: AoDaDou
"""

__all__ = ['RecommendItem', 'Container']


# 推荐的物品类
class RecommendItem(object):
    def __init__(self, itemid, score, reason={}):
        """
        推荐物品的类
        :param id: 推荐物品的ID
        :param name: 推荐物品的名称，用于对外展示
        :param score: 推荐物品的得分
        :param reason: 推荐物品的理由，字典形式，{engine:reason}
        :param engine: 推荐物品的引擎

        """
        self.id = itemid
        self.name = 'Item'+str(itemid)
        self.score = score
        self.reason = reason
        self.engine = list(reason.keys())[0]
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name



# 存放数据的容器类
class Container(object):
    def __init__(self, datafunction, trainSet):
        self.Item_Users, self.Item_times, self.Item_vectors, self.User_Items = datafunction(trainSet)
        


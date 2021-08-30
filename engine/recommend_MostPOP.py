# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:21:01 2021

@author: ecupl
"""

from base import RecommendItem
from utils import quickSort


__all__ = ['FavoriteRecommend']


# 用户点击量/得分最高的物品推荐
class FavoriteRecommend(object):
    """
    基于用户得分最高的物品进行再次推荐
    """
    def __init__(self):
        self.topN = 0               # 推荐前N个产品
        self.engine = 'Favoraite'   # 用户最欢的物品推荐
        
        
    def transform(self, topN, user, havingItems=None):
        """
        单个用户的物品推荐，要么输入用户ID，要么输入用户已经拥有的物品列表

        Parameters
        ----------
        topN : int
            需要推荐的物品数量
        user : int or string
            需要推荐的用户ID.
        havingItems : list
            单个用户已经拥有的物品列表，默认为None.

        Returns
        -------
        Recommendrank : list[RecommendItem, RecommendItem, ......]
            推荐物品的列表，其中的物品封装成了类，包含物品ID、推荐理由、推荐得分等等属性。

        """
        # 判断havingItems
        if havingItems is None:
            return []
        else:
            pass
        # 对用户喜欢的物品按照得分进行倒排序
        favItems = quickSort(havingItems.items(), key=lambda x: x[1], reverse=True)
        # 封装成推荐物品类
        Recommendrank = [RecommendItem(item, score, {self.engine:'Favorite Used'}) for item, score in favItems[:topN]]
        return Recommendrank


    def recommend(self, topN, User_Items):
        """
        对用户-物品矩阵中的所有用户进行推荐。

        Parameters
        ----------
        topN : int
            需要推荐的物品数量
        User_Items : dict
            用户——物品矩阵

        Returns
        -------
        RecommendDict : dict
            每个用户的推荐列表，{用户1：[(推荐物品1， 分数， 理由), (推荐物品2， 分数， 理由), ...]}

        """
        self.topN = topN        # 推荐前N个产品
        RecommendDict = dict()    # 推荐的字典
        
        for user, items in User_Items.items():
            Recommendrank = self.transform(topN, user, items)
            RecommendDict[user] = Recommendrank
        # self.RecommendDict = RecommendDict
        return RecommendDict
    
    
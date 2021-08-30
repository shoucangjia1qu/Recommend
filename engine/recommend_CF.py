# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 09:20:29 2021

@author: AoDaDou
"""

import numpy as np
from base import RecommendItem

__all__ = ['ItemCF']


# 协同过滤的类
class ItemCF(object):
    """
    基于物品相似度的推荐引擎
    """

    def __init__(self):
        """
        ItemCF‘s function descirbe:
        1. fit() : 训练物品相似度的矩阵
        2. transform() : 单个用户的物品推荐
        3. recommend() : 所有客户的物品推荐
        """
        self.topN = 0       # 推荐前N个产品
        self.K = 0          # 选择相邻数
        self.engine = 'ItemCF'


    def fit(self, Item_Users, Item_vectors):
        """
        训练物品相似度矩阵

        Parameters
        ----------
        Item_Users : dict
            物品——用户评分字典, {I1:{U1:score, U2:score, ...}, 
                                I2:{U2:score, ...}, 
                                ......}
        Item_vectors : dict
            物品向量字典, {I1:[score1, score2, ...],
                          I2:[score2, ...],
                          ......}
        
        Returns
        -------
        Item_sim : dict
            物品——物品相似度字典, {I1:{I2:W12, I3:W13, ......}, ......}

        """
        # 根据Item_user矩阵，统计Item_Item的点乘
        IIdot = dict()
        IIsim = dict()
        # 遍历Item_users矩阵
        for itemA, usersA in Item_Users.items():
            # 直接取出物品对应的所有用户
            userA = set(usersA.keys())
            if itemA not in IIdot.keys():
                IIdot[itemA] = dict()
                IIsim[itemA] = dict()
            for itemB, usersB in Item_Users.items():
                if itemA == itemB:
                    continue
                IIdot[itemA][itemB] = 0
                # 找到AB物品的用户交集，并计算点乘值
                userB = set(usersB.keys())
                userAB = userA.intersection(userB)
                if not userAB:
                    continue
                # 求AB物品间的点乘
                for user in userAB:
                    IIdot[itemA][itemB] += usersA[user] * usersB[user]
                # 求AB物品间的相似度
                IIsim[itemA][itemB] = round(IIdot[itemA][itemB] / (np.linalg.norm(Item_vectors[itemA]) * np.linalg.norm(Item_vectors[itemB])), 5)
        # 物品相似度矩阵
        self.Item_sim = IIsim
        return



    def transform(self, topN, K, user, havingItems=None):
        """
        单个用户的物品推荐，要么输入用户ID，要么输入用户已经拥有的物品列表

        Parameters
        ----------
        topN : int
            需要推荐的物品数量
        K : int
            物品相似度的近邻数量
        user : int or string
            需要推荐的用户ID.
        havingItems : list
            单个用户已经拥有的物品列表，默认为None.

        Returns
        -------
        Recommendrank : list[RecommendItem, RecommendItem, ......]
            推荐物品的列表，其中的物品封装成了类，包含物品ID、推荐理由、推荐得分等等属性。

        """
        rank = dict()
        reason = dict()
        # 判断havingItems
        if havingItems is None:
            return []
        else:
            pass
        # 正式开始遍历已有物品，根据物品相似度进行推荐。
        for item in havingItems:
            for similarItem, wi in sorted(self.Item_sim[item].items(), key=lambda x: x[1], reverse=True)[:K]:
                if similarItem in havingItems:
                    continue
                if similarItem not in rank.keys():
                    rank[similarItem] = 0
                    reason[similarItem] = dict()
                # 加入每个推荐物品的权重
                rank[similarItem] += 1 * wi
                # 加入推荐物品的解释理由
                if item not in reason[similarItem].keys():
                    reason[similarItem][item] = 0
                reason[similarItem][item] += 1 * wi
        rank = sorted(rank.items(), key=lambda x: x[1], reverse=True)[:topN]
        # 选出推荐的物品的推荐理由
        Recommendrank = [RecommendItem(item, score, {self.engine:reason[item]}) for item, score in rank]
        return Recommendrank


    def recommend(self, topN, K, User_Items):
        """
        对用户-物品矩阵中的所有用户进行推荐。

        Parameters
        ----------
        topN : int
            需要推荐的物品数量
        K : int
            物品相似度的近邻数量
        User_Items : dict
            用户——物品矩阵

        Returns
        -------
        RecommendDict : dict
            每个用户的推荐列表，{用户1：[(推荐物品1， 分数， 理由), (推荐物品2， 分数， 理由), ...]}

        """
        self.topN = topN        # 推荐前N个产品
        self.K = K              # 选择相邻数
        RecommendDict = dict()    # 推荐的字典
        
        for user, items in User_Items.items():
            Recommendrank = self.transform(topN, K, user, items.keys())
            RecommendDict[user] = Recommendrank
        # self.RecommendDict = RecommendDict
        return RecommendDict






    
    
    
    


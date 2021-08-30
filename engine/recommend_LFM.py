# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from base import RecommendItem

__all__ = ['LFMRecommend']

class LFMRecommend(object):
    def __init__(self, learning_rate, factor_nums, n_iters, neg_pos_ratio, L2, threshold=0.0001):
        """
        LFM‘s function descirbe:
        1. fit() : 训练用户、物品的矩阵
        2. transform() : 单个用户的物品推荐
        3. recommend() : 所有客户的物品推荐
        """
        self.learning_rate = learning_rate          # 学习率
        self.L2 = L2                                # L2正则系数
        self.factor = factor_nums                   # 隐矩阵列数
        self.n_iters = n_iters                      # 迭代次数
        self.neg_pos_ratio = neg_pos_ratio          # 负样本/正样本的比例
        self.threshold = threshold                  # 最小误差（作为训练停止条件）
        self.engine = 'LFM'
        self.lossList = []                          # 误差列表
        
    
    # 取正负样本，正样本就是有评分的物品，负样本是很热门但是却没有评分的物品
    # 因为很热门却没有评分的物品，会显示出该客户更加没兴趣
    def __get_sample(self, userid, postiveItems):
        # 正样本添加标签为1
        samples = [(i, 1) for i in postiveItems]
        postive_nums = len(postiveItems)
        # 从物品池中添加负样本，并添加标签为0
        for i in self.items_pool:
            # 若样本数量达到负正样本的要求，则停止抽样
            if len(samples) > int((self.neg_pos_ratio+1) * postive_nums):
                break
            # 若样本在正样本中出现过，则跳过抽样
            if i in postiveItems:
                continue
            # 添加为负样本
            samples.append((i, 0))
        return samples

    
    # 计算物品对应物品的分值
    def predict(self, user_matrix, item_matrix):
        return np.dot(user_matrix, item_matrix.T)
    
    
    # 计算整体误差
    def __cal_loss(self, user_matrix, item_matrix):
        # 预测整体的用户-物品得分
        predMatrix = self.predict(user_matrix, item_matrix)
        euiMatrix = self.train_matrix.values - predMatrix
        loss = np.power(euiMatrix, 2).sum() + self.L2 * np.power(np.linalg.norm(user_matrix), 2) + self.L2 * np.power(np.linalg.norm(item_matrix), 2)
        return loss
    
    
    # 训练用户隐矩阵、物品隐矩阵
    def fit(self, User_Items, Item_times):
        # 生成真实的用户-物品矩阵，0/1矩阵
        self.train_matrix = pd.DataFrame(User_Items).T.notnull()*1
        userList = list(self.train_matrix.index)
        itemList = list(self.train_matrix.columns)
        n_users, n_items = self.train_matrix.shape
        # 生成物品池，按照物品次数从高到底排序
        self.items_pool = [i[0] for i in sorted(Item_times.items(), key=lambda x: x[1], reverse=True)]
        # 初始化用户隐矩阵和物品隐矩阵
        # UserMatrix = np.zeros((n_users, self.factor))
        # ItemMatrix = np.zeros((n_items, self.factor))
        UserMatrix = np.random.rand(n_users, self.factor)*0.01 - 0.005
        ItemMatrix = np.random.rand(n_items, self.factor)*0.01 - 0.005
        # 计算并保存初始误差
        self.lossList.append(self.__cal_loss(UserMatrix, ItemMatrix))
        # 开始训练
        for epoch in range(self.n_iters):
            print(f">>>第{epoch}轮迭代")
            for useridx, userid in enumerate(userList):
                # 1. 获取正样本, [item0, item1, ...]
                postiveItems = User_Items[userid].keys()
                # 2. 生成正负样本的训练数据集, [(item0, label0), (item1, label1), ...]
                allSamples = self.__get_sample(userid, postiveItems)
                allSamplesIndex = [itemList.index(i) for i, s in allSamples]
                allSamplesScore = np.array([s for i, s in allSamples])
                # 3. 批量预测某个用户对应物品的分值
                predScore = self.predict(UserMatrix[useridx, :], ItemMatrix[allSamplesIndex, :])
                # 4. 计算userid选中样本的误差
                euiArray = allSamplesScore - predScore
                # 5. 批量迭代新的矩阵
                ## 用户隐矩阵一行更新多次
                # UserMatrix[useridx, :] += self.learning_rate * (np.multiply(euiArray.reshape(-1, 1), ItemMatrix[allSamplesIndex, :]) - self.L2 * UserMatrix[useridx, :]).sum(axis=0)
                ## 物品隐矩阵多行更新一次
                # ItemMatrix[allSamplesIndex, :] += self.learning_rate * (np.multiply(euiArray.reshape(-1, 1), UserMatrix[useridx, :].reshape(1, -1)) - self.L2 * ItemMatrix[allSamplesIndex, :])
                
                # 5. 根据选中的样本误差逐次迭代
                for order, itemidx in enumerate(allSamplesIndex):
                    eui = euiArray[order]
                    UserMatrix[useridx, :] += self.learning_rate * (eui * ItemMatrix[itemidx, :] - self.L2 * UserMatrix[useridx, :])
                    ItemMatrix[itemidx, :] += self.learning_rate * (eui * UserMatrix[useridx, :] - self.L2 * ItemMatrix[itemidx, :])
            # 6. 计算整体误差
            loss = self.__cal_loss(UserMatrix, ItemMatrix)
            print(f"误差为{loss}")
            self.lossList.append(loss)
            self.learning_rate = round(self.learning_rate*0.9, 2)
            # 7. 设置停止条件，误差低于阈值，前后两次误差基本不变
        self.itemList =  itemList
        self.UserMatrix = UserMatrix
        self.ItemMatrix = ItemMatrix
        self.MatrixScore = pd.DataFrame(data=self.predict(UserMatrix, ItemMatrix), index=userList, columns=itemList)
        return

        
    def transform(self, topN, user, havingItems=None):
        """
        单个用户的LFM物品推荐

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
        rank = dict()
        reason = dict()
        # 判断havingItems
        if havingItems is None:
            return []
        else:
            pass
        items_score = self.MatrixScore.loc[user].values
        items_score_idx = items_score.argsort()[::-1]
        for i in range(len(items_score)):
            # 选出推荐的单个物品
            recommend_item = self.itemList[items_score_idx[i]]
            # 在已有物品中，就不推荐了
            if recommend_item in havingItems:
                continue
            # 达到推荐数量或者分数小于0，停止选取物品
            if (len(rank) >= topN) or (items_score[items_score_idx[i]]<0):
                break
            # 继续保存推荐物品
            rank[recommend_item] = items_score[items_score_idx[i]]
            reason[recommend_item] = items_score[items_score_idx[i]]
        # 选出推荐的物品的推荐理由
        Recommendrank = [RecommendItem(item, score, {self.engine:reason[item]}) for item, score in rank.items()]
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
            Recommendrank = self.transform(topN, user, items.keys())
            RecommendDict[user] = Recommendrank
        # self.RecommendDict = RecommendDict
        return RecommendDict











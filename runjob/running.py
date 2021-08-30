# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 19:12:49 2021

@author: ecupl
"""

import numpy as np
import pandas as pd
import pickle


__all__ = ['loadingData', 'combineRecommend', 'savingData']

# 读取数据
def loadingData(path, idColumns, startColumn, endColumn, dropRows=None):
    """
    要注意给出数据的id名称；
    要注意我们需要数据的开始和结束的列名，
    要注意给出数据给出的行名，如果有中文，需要删除那一行
    
    """
    df = pd.read_csv(path)
    # 删除不用的行数
    if dropRows is not None:
        df.drop(dropRows, axis=0, inplace=True)
    df.fillna(0, inplace=True)
    userList = list(df[idColumns])
    itemList = list(df.columns)[list(df.columns).index(startColumn):list(df.columns).index(endColumn)+1]
    value = df[itemList].to_numpy().astype(float)*1 + df[[i+'_jy' for i in itemList]].to_numpy().astype(float)*3
    # 转成密集矩阵(按照具体的用户、物品输出)
    row, column = np.nonzero(value!=0)
    tup1 = tuple(zip([userList[i] for i in row], [itemList[i] for i in column], value[(value!=0)].flatten()))
    # 转成密集矩阵(按照索引输出)
    # tup1 = tuple(*zip(np.nonzero(value!=0), value[(value!=0)].flatten()))
    # return np.array(tup1, dtype=int)
    return pd.DataFrame(tup1, columns=['user', 'item', 'ratings'])


# 合并推荐物品        
def combineRecommend(userList, *args, blackList=[]):
    res = dict()
    for u in userList:
        Recommend = []
        RecommandID = []
        # 1. 遍历多个推荐引擎
        for engine in args:
            # 1.1 推荐引擎中无该客户，则跳过
            if u not in engine.keys():
                continue
            # 1.2 遍历该推荐引擎的推荐物品
            for i in engine[u]:
                # 1.2.1 物品在黑名单中，则跳过
                if i.id in blackList:
                    continue
                # 1.2.2 物品重复了，合并信息，包括engine, reason, 
                if i.id in RecommandID:
                    Recommend[RecommandID.index(i.id)].engine += '+' + i.engine
                    Recommend[RecommandID.index(i.id)].reason.update(i.reason)
                    continue
                # 1.2.3 正常状态下，保存信息
                Recommend.append(i)
                RecommandID.append(i.id)
            # 将推荐物品列表赋值给res
            res[u] = Recommend   
    return res


# 保存推荐结果
def savingData(path, RecommendItems):
    # 序列化保存
    with open(path+"/RecommendItems.dat", 'wb') as f1:
        pickle.dump(RecommendItems, f1)
        
    # 只保存userID+推荐物品ID
    RecommendList = [str(userID) + "," + ",".join([item.id for item in items]) for userID, items in RecommendItems.items()]
    RecommendStr = "\n".join(RecommendList)
    with open(path+"/RecommendStr3.txt", 'w') as f2:
        f2.write(RecommendStr)
    return

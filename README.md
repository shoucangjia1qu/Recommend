## 一、文档结构
**|-- recommend**  
&emsp;**|-- main.py**  
&emsp;**|-- base**  
&emsp;&emsp;|-- \_\_init\_\_.py  
&emsp;&emsp;|-- baseclass.py  
&emsp;**|-- utils**  
&emsp;&emsp;|-- \_\_init\_\_.py  
&emsp;&emsp;|-- recommend_review.py  
&emsp;&emsp;|-- dataprocess.py  
&emsp;**|-- engine**  
&emsp;&emsp;|-- \_\_init\_\_.py  
&emsp;&emsp;|-- recommend_ItemCF.py  
&emsp;&emsp;|-- recommend_LFM.py  
&emsp;&emsp;|-- recommend_MostPOP.py  
&emsp;**|-- runjob**  
&emsp;&emsp;|-- \_\_init\_\_.py  
&emsp;&emsp;|-- running.py  
&emsp;**|-- dataSet**  
  
  
  
## 二、文档介绍
### 1. base
**一些基础功能**
- baseclass.py——用于存放基础类
    - RecommendItem：推荐物品类。  
    **属性包括：** 推荐物品的ID，名称，得分，理由，引擎。
    - Container：数据容器类。  
    **属性包括：** 物品-用户-分数矩阵(dict)，物品喜欢人数(dict)，物品向量矩阵(dict)，用户-物品-分数矩阵(dict)。  
  
  
### 2. utils
**一些通用功能**
- dataprocess.py——数据处理函数
    - datachange：通过输入numpy密集矩阵[user, item, rat]，转换成推荐需要的各种数据，之后会存放在base.baseclass.Container类中。  
    - quickSort：对数组进行快排序。  
  
  
- recommend_review.py——推荐指标回测的函数
    - get_testitems：获取单个客户测试集中的物品数组。  
    - singleevaluate：计算单个客户推荐的命中数量。  
    - evaluate：计算全部推荐的一些指标，包括命中数、查准率、查全率、覆盖率、流行度。  
  
  
### 3. engine
**核心推荐引擎部分**
- recommend_CF.py——协同过滤的算法包
    - ItemCF：基于物品相似度的协同过滤算法类。  
    **属性包括：** 推荐物品数(TopN)，相邻物品数(K)，物品相似度矩阵(Item_sim)等。  
    **方法包括：**  
        1. 训练(fit):根据物品-用户-分数矩阵(dict)，物品向量矩阵(dict)训练出物品相似度矩阵(dict)。  
        2. 单用户推荐(transform):根据训练出来的物品相似度矩阵，给定userid输出推荐物品的数组。  
        3. 整体的推荐(recommend):对全量有行为的客户进行推荐，并保存为字典。  
  
  
- recommend_LFM.py——隐语义模型的算法包
    - LFMRecommend：基于隐语义模型的推荐算法类，尚未完成。  
    **属性包括：**   
    **方法包括：**  
  
  
- recommend_MostPOP.py——物品流行度的推荐  
    - FavoriteRecommend：基于每个用户物品流行度的推荐类。  
    **属性包括：** 推荐物品数(TopN)等。  
    **方法包括：**    
        1. 单用户推荐(transform):根据用户-物品-分数矩阵(dict)，给定userid输出最热门物品的数组。  
        2. 整体的推荐(recommend):对全量有行为的客户进行推荐，并保存为字典。
  
  
### 4. runjob
**一些项目运行用到的特定功能**
- running.py——项目运行用到的函数
    - loadingData：稀疏矩阵的数据导入并进行处理，最终输出密集矩阵[user, item, rat]。  
    - combineRecommend：合并多个引擎的推荐数据，去重、去黑，行程最终的用户——推荐物品矩阵(dict)。  
    - savingData：保存推荐结果至本地。
  
  
### 5. dataSet
**数据集**
  
  
### 6. main.py
**主要就是main函数，具体见下面的执行逻辑。**
  
  
  
## 三、main函数执行逻辑
### 参数说明：
- train_path：训练集数据路径；
- res_path：推荐结果保存路径；
- test_path：测试集结果路径，默认为空字符串，若为空字符串，则表示没有以下的评价过程。
  
  
### 1. 训练过程：
- 通过runjob.running.loadingData函数读取稀疏矩阵，转换成密集矩阵[user, item, rat]；
- 通过utils.dataprocess.datachange函数对数据进行转换，变成物品-用户-分数矩阵(dict)，物品喜欢人数(dict)，物品向量矩阵(dict)，用户-物品-分数矩阵(dict)，并存入base.baseclass.Container容器中；
- 通过engine中的协同过滤(recommend_CF.ItemCF)、隐语义(recommend_LFM.LFMRecommend)、流行度(recommend_MostPOP.FavoriteRecommend)进行训练和推荐；
- 通过runjob.running.combineRecommend进行整合，并输出res推荐结果。
  
  
### 2. 评价过程：
- 通过runjob.running.loadingData函数读取测试数据；
- 通过utils.recommend_review.evaluate函数对推荐结果进行命中数、查准率、查全率、覆盖率、流行度等指标的评价。
  
  
### 3. 保存结果：
- 通过runjob.running.savingData函数将结果保存至本地。





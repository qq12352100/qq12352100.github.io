'''
pip install -U jiagu
'''
import jiagu

text = "深度学习是人工智能的核心技术"
words = jiagu.seg(text)
print(words)
text = '姚明1980年9月12日出生于上海市徐汇区，祖籍江苏省苏州市吴江区震泽镇，前中国职业篮球运动员，司职中锋，现任中职联公司董事长兼总经理。'
knowledge = jiagu.knowledge(text)
print(knowledge)
docs = [
"苹果是一种常见的水果，富含维生素和膳食纤维",
"香蕉是热带水果，含有丰富的钾元素，有助于缓解疲劳",
"水果分类研究：浆果、核果和柑橘类水果的营养价值比较",
"如何挑选新鲜的水果？从颜色、气味和硬度三个方面教你选购技巧",
"芒果的栽培技术及病虫害防治方法分享",
"不同成熟度的水果在储存过程中糖分和酸度的变化研究",
"水果榨汁与直接食用的营养差异分析",
"进口水果与本地水果在价格和口感上的对比评测"
]
cluster = jiagu.text_cluster(docs)
for group_id, values in cluster.items():
    print(group_id, values)
text = '我不喜欢吃苹果。'
sentiment = jiagu.sentiment(text)
print(sentiment)
text = '我特别喜欢吃香蕉。'
sentiment = jiagu.sentiment(text)
print(sentiment)
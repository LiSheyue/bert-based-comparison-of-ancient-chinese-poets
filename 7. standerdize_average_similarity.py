import pandas as pd


# 读取JSON数据
data = pd.read_json('data/average_similarity.json')

# 提取需要标准化的列
col_to_standerdize = data['average_similarity']

# 执行max-min标准化
standerdized = (col_to_standerdize - col_to_standerdize.min()) / (col_to_standerdize.max() - col_to_standerdize.min())

# 更新原数据
data['average_similarity'] = standerdized

# 输出结果
data.to_json('data/average_similarity_standerdized.json', orient='records', indent=4, force_ascii=False)
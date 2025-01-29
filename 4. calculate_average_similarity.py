from collections import defaultdict
import json

# 用于存储相同诗人对的相似度值
similarity_dict = defaultdict(list)

with open(r"data/poem_similarities.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split('\t')
        similarity = float(parts[0])
        poet_pair = parts[2]
        if ',' in poet_pair:
            sorted_pair = tuple(sorted(map(int, poet_pair.split(','))))
            similarity_dict[sorted_pair].append(similarity)
        else:
            single_id = int(poet_pair)
            similarity_dict[(single_id, single_id)].append(similarity)

# 计算平均值
average_similarities = {}
for pair, sim_list in similarity_dict.items():
    average = sum(sim_list)/len(sim_list)
    average_similarities[pair] = average

# 按照从高到低排序
sorted_average_similarities = sorted(average_similarities.items(), key=lambda x: x[1], reverse=True)

with open('data/average_similarity.json', 'w', encoding='utf-8') as f:
    json.dump([{"poet_pair": list(pair), "average_similarity": value} for pair, value in sorted_average_similarities], f, ensure_ascii=False, indent=4)
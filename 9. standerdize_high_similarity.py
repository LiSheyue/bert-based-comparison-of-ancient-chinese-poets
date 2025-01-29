import json

# 读取作者作品数量
with open(r'data/poet_work_count.json', 'r', encoding='utf-8') as f:
    author_work_count = json.load(f)

# 读取作者对共现次数
with open(r'data/high_similarity_relationship.json', 'r', encoding='utf-8') as f:
    author_pairs_count = json.load(f)

# 标准化数据
new_format_data = []
for pair, count in author_pairs_count.items():
    if ',' in pair:  # 如果是两个作者的配对
        author_ids = pair.split(',')
        count_a = author_work_count.get(author_ids[0], 1)
        count_b = author_work_count.get(author_ids[1], 1)
        denominator = count_a * count_b
        standardized_value = count / denominator
    else:  # 如果是单个作者
        author_id = pair
        count_self = author_work_count.get(author_id, 1)
        standardized_value = count / (count_self ** 2)

    if ',' in pair:
        poet_pair = [int(author_id) for author_id in author_ids]
    else:
        poet_pair = [int(author_id), int(author_id)]

    new_format_data.append({
        "poet_pair": poet_pair,
        "high_similarity": standardized_value
    })

# 输出标准化后的数据
with open('data/high_similarity_standardized.json', 'w', encoding='utf-8') as json_file:
    json.dump(new_format_data, json_file, ensure_ascii=False, indent=4)
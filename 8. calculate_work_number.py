import json

author_work_count = {}

with open(r'data/mid_tang_poems.json', 'r', encoding='utf-8') as f:
    poems = json.load(f)
    for poem in poems:
        poet_id = poem["poet_id"]
        author_work_count[poet_id] = author_work_count.get(poet_id, 0) + 1

# 将统计结果保存为json文件
with open('data/poet_work_count.json', 'w', encoding='utf-8') as outfile:
    json.dump(author_work_count, outfile, ensure_ascii=False, indent=4)
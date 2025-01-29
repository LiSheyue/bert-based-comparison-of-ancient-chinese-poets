import json
from collections import Counter

def read_similarities(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    return lines

if __name__ == "__main__":
    input_file_path = "data/high_similarity_poems.txt"
    pairs_counter = Counter()

    lines = read_similarities(input_file_path)
    for line in lines:
        try:
            parts = line.split("\t")
            pair = parts[2]
            # 将每对组合转换为frozenset，确保顺序不影响统计
            poets = pair.split(",")
            pair_set = frozenset(poets)  # 使用frozenset确保顺序不影响统计
            pairs_counter[tuple(sorted(pair_set))] += 1  # 将frozenset转换为排序后的元组
        except (IndexError, ValueError):
            continue

    # 将计数转换为所需的格式
    sorted_pairs = pairs_counter.most_common()

    # 格式化为要求的字符串形式
    result = {",".join(pair): count for pair, count in sorted_pairs}  # 保留原始计数
    with open('data/high_similarity_relationship.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

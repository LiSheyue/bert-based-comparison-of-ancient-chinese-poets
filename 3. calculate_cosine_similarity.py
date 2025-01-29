import json
import os
import torch
import torch.nn.functional as F
from tqdm import tqdm
import itertools

input_embeddings_path = r"data/poem_embeddings.json"
output_similarity_path = r"data/poem_similarities.txt"

def load_embeddings(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 计算余弦相似度
def calculate_cosine_similarity(embedding1, embedding2):
    tensor1 = torch.tensor(embedding1)
    tensor2 = torch.tensor(embedding2)
    return F.cosine_similarity(tensor1.unsqueeze(0), tensor2.unsqueeze(0)).item()

def process_similarities(input_path, output_path):
    embeddings_data = load_embeddings(input_path)
    similarities = []

    pairs = list(itertools.combinations(embeddings_data, 2))

    for poem1, poem2 in tqdm(pairs, desc="计算相似度", total=len(pairs)):
        try:
            poem_id1 = poem1['poem_id']
            poet_id1 = poem1['poet_id']
            embedding1 = poem1['embedding']

            poem_id2 = poem2['poem_id']
            poet_id2 = poem2['poet_id']
            embedding2 = poem2['embedding']

            similarity = calculate_cosine_similarity(embedding1, embedding2)

            similarities.append((similarity, {poem_id1, poem_id2}, {poet_id1, poet_id2}))

        except Exception as e:
            print(f"计算诗歌 {poem_id1} 和 {poem_id2} 的相似度时发生错误: {e}")

    with open(output_path, 'w', encoding='utf-8') as file:
        for sim in similarities:
            similarity, poem_ids, poet_ids = sim
            poem_ids_str = ",".join(map(str, poem_ids))
            poet_ids_str = ",".join(map(str, poet_ids))
            file.write(f"{similarity:.4f}\t{poem_ids_str}\t{poet_ids_str}\n")

if __name__ == "__main__":
    if not os.path.exists(input_embeddings_path):
        print(f"输入的诗歌向量文件未找到: {input_embeddings_path}")
    else:
        process_similarities(input_embeddings_path, output_similarity_path)
        print(f"相似度已保存到 {output_similarity_path}")

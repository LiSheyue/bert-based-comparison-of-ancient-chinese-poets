import json
import os
from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F
from tqdm import tqdm

input_path = r"data/mid_tang_poems.json"
output_path = r"data/poem_embeddings.json"

# 加载模型
tokenizer = BertTokenizer.from_pretrained("qixun/bert-chinese-poem")
model = BertModel.from_pretrained("qixun/bert-chinese-poem")

# 获取每首诗歌的向量表示
def get_embedding(poem, max_length=512):
    tokens = tokenizer(poem, return_tensors='pt', padding=True, truncation=False)
    input_ids = tokens['input_ids'][0]
    
    # 将超长文本分割
    num_chunks = (len(input_ids) + max_length - 1) // max_length
    embeddings = []
    
    for i in range(num_chunks):
        chunk_ids = input_ids[i * max_length:(i + 1) * max_length]
        inputs = {'input_ids': chunk_ids.unsqueeze(0), 'attention_mask': torch.ones_like(chunk_ids).unsqueeze(0)}
        
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1))
    
    final_embedding = torch.stack(embeddings).mean(dim=0)
    return final_embedding

def process_dataset(input_path, output_path):

    with open(input_path, 'r', encoding='utf-8') as file:
        poems = json.load(file)
    
    results = []

    for poem in tqdm(poems, desc="处理诗歌"):
        try:
            poem_id = poem['id']
            poet_id = poem['poet_id']
            poem_text = poem['poem_text']

            embedding = get_embedding(poem_text)
            
            # 保存结果
            results.append({
                'poem_id': poem_id,
                'poet_id': poet_id,
                'embedding': embedding.squeeze().tolist()
            })
        except Exception as e:
            print(f"处理诗歌 ID {poem['id']} 时发生错误: {e}")

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    if not os.path.exists(input_path):
        print(f"未找到文件: {input_path}")
    else:
        process_dataset(input_path, output_path)
        print(f"嵌入向量已保存到 {output_path}")
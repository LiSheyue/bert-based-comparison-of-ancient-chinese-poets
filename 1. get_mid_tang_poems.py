import json
input_file = 'data/poetry_data.json'
output_file = 'data/mid_tang_poems.json'
author_ids_file = 'data/author_ids.json'
# 作者ID字典
author_ids = {
    "韦应物": 109,
    "刘长卿": 182,
    "顾况": 153,
    "李益": 157,
    "韩愈": 202,
    "孟郊": 106,
    "李贺": 95,
    "刘禹锡": 232,
    "柳宗元": 117,
    "张籍": 94,
    "王建": 121,
    "元稹": 108,
    "白居易": 155
}

try:
    # 将作者ID字典写入文件
    with open(author_ids_file, 'w', encoding='utf-8') as id_file:
        json.dump(author_ids, id_file, ensure_ascii=False, indent=4)

    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # 筛选符合条件的诗歌
    filtered_poems = [poem for poem in data if poem.get("poet_id") in author_ids.values()]

    # 将筛选结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(filtered_poems, outfile, ensure_ascii=False, indent=4)

    print(f"筛选完成，共筛选出 {len(filtered_poems)} 首诗歌，已保存到 {output_file}。")
    print(f"作者ID字典已保存到 {author_ids_file}。")

except FileNotFoundError:
    print(f"文件未找到：{input_file}")
except json.JSONDecodeError:
    print("JSON 文件格式错误。")
except Exception as e:
    print(f"发生错误：{e}")

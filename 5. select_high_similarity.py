def read_similarities(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())
    return lines


if __name__ == "__main__":
    input_file_path = r"data/poem_similarities.txt"
    output_file_path = r"data/high_similarity_poems.txt"
    all_lines = read_similarities(input_file_path)
    high_similarity_lines = []

    for line in all_lines:
        try:
            similarity = float(line.split("\t")[0])
            if similarity > 0.6:
                high_similarity_lines.append(line)
        except (IndexError, ValueError):
            continue

    with open(output_file_path, 'w', encoding='utf-8') as out_file:
        for line in high_similarity_lines:
            out_file.write(line + '\n')
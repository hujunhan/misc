import csv
import docx

# 读取Word文档
doc_filename = "/Users/hu/Downloads/Phloe_DEG_1104_GO分类.docx"
doc = docx.Document(doc_filename)
text = [p.text for p in doc.paragraphs]
# 读取文本
data = "\n".join(text)

# 将数据按类别划分
groups = data.strip().split("（")
group_data = {}

for group in groups[1:]:
    lines = group.strip().split("\n")
    group_number = lines[0].strip("）")
    genes = lines[1].split("/")
    group_data[group_number] = genes

# 将数据写入CSV文件
csv_filename = "gene_groups.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Group", "Gene"])

    for group, genes in group_data.items():
        for gene in genes:
            writer.writerow([group, gene])

print(f"数据已成功写入 {csv_filename} 文件。")

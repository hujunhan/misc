## 别人做好的工具包
import glob
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

pre_path = "/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes"
md_path = sorted(glob.glob(pre_path + "/**/*.md", recursive=True))

characters_count = 0
characters__nospace_count = 0
chinese_count = 0
english_count = 0

all_count_dict = defaultdict(int)

# 函数1，输入一个字符，如果是中文字符，就返回True，如果不是，就返回False
def is_chinese(char):
    if "\u4e00" <= char <= "\u9fff":
        return True
    else:
        return False


def word_count(text):
    characters = len(text)
    chars_no_spaces = sum([not c.isspace() for c in text])
    chinese_characters = sum([is_chinese(c) for c in text])
    no_chinese_text = [" " if is_chinese(c) else c for c in text]
    english_word_count = len("".join(no_chinese_text).split())
    return characters, chars_no_spaces, chinese_characters, english_word_count


# 对每个在md_path中的路径，我把他叫做path
for path in md_path:
    md_name = path.split("/")[-1]
    f = open(path, "r")
    data = f.read()

    ## Count by time
    for line in data.split("\n"):
        if "date:" in line:
            # print(line.split(' ')[1])
            ## Convert date string to datetime object
            ## Format of date string: 2021-01-01
            date = datetime.strptime(line.split(" ")[1], "%Y-%m-%d")
            break

    # data=re.sub(r'[\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+', "", data)
    a, b, c, d = word_count(data)

    all_count_dict[date] += c + d

    characters_count += a
    characters__nospace_count += b
    chinese_count += c
    english_count += d
    # print(f'{md_name} {num}')
    f.close()

print(f"Number of Markdown Notes:         {len(md_path)}")
print(f"Total Character Count:            {characters_count}")
print(f"Total Character (No Space) Count: {characters__nospace_count}")
print(f"Total Chinese Character Count:    {chinese_count}")
print(f"Total English Word Count:         {english_count}")
print(f"Total Word Count:                 {chinese_count+english_count}")

## sort by date
all_count_dict = dict(sorted(all_count_dict.items()))
# print(all_count_dict)
## count the culmulative sum of words by adding the previous day's word count
previous_word_count = 0
for key in all_count_dict.keys():
    all_count_dict[key] += previous_word_count
    previous_word_count = all_count_dict[key]

## plot the word count by date
fig, ax = plt.subplots()
x = list(all_count_dict.keys())
x = [i.toordinal() for i in x]
y = list(all_count_dict.values())

## get the x ticks, divide the x axis into 5 parts
max_x = max(x)
min_x = min(x)
all_days = max_x - min_x
x_ticks = [min_x + all_days * i // 4 for i in range(5)]  ## get the x ticks
x_ticks_label = [
    datetime.fromordinal(min_x + all_days * i // 4).strftime("%Y-%m-%d")
    for i in range(5)
]
x_ticks = [i - min_x for i in x_ticks]  ## make the x ticks start from 0

x = [i - min_x for i in x]
ax.plot(x, y)
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_ticks_label)
# Use numpy to fit the data with a line and plot it
# and print the formula of the fitted line
ax.plot(x, np.poly1d(np.polyfit(x, y, 1))(x))
ax.text(
    0.5,
    0.5,
    "y=%.1fx+(%.1f)" % (np.polyfit(x, y, 1)[0], np.polyfit(x, y, 1)[1]),
    transform=ax.transAxes,
)

plt.title("Word Count by Date")
plt.show()

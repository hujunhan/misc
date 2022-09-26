## 别人做好的工具包
import glob


pre_path='/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes'
md_path=sorted(glob.glob(pre_path+'/**/*.md',recursive=True))

characters_count=0
characters__nospace_count=0
chinese_count=0
english_count=0

# 函数1，输入一个字符，如果是中文字符，就返回True，如果不是，就返回False
def is_chinese(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    else:
        return False

def word_count(text):
    characters=len(text)
    chars_no_spaces = sum([not c.isspace() for c in text])
    chinese_characters=sum([is_chinese(c) for c in text])
    no_chinese_text=[' ' if is_chinese(c) else c for c in text]
    english_word_count=len(''.join(no_chinese_text).split())
    return characters,chars_no_spaces,chinese_characters,english_word_count
# 对每个在md_path中的路径，我把他叫做path
for path in md_path:
    md_name=path.split('/')[-1]
    f=open(path,'r')
    data=f.read()
    # data=re.sub(r'[\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+', "", data)
    a,b,c,d=word_count(data)
    characters_count+=a
    characters__nospace_count+=b
    chinese_count+=c
    english_count+=d
    # print(f'{md_name} {num}')
    f.close()

print(f'Number of Markdown Notes:         {len(md_path)}')
print(f'Total Character Count:            {characters_count}')
print(f'Total Character (No Space) Count: {characters__nospace_count}')
print(f'Total Chinese Character Count:    {chinese_count}')
print(f'Total English Word Count:         {english_count}')
print(f'Total Word Count:                 {chinese_count+english_count}')
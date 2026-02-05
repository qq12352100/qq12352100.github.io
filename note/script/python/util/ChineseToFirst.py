
'''
汉字转拼音首字母
pip install pypinyin
'''
from pypinyin import lazy_pinyin, Style

# 汉字转拼音（小写）
def toLowAll(text):
    return ' '.join(lazy_pinyin(text))
    
# 汉字转拼音（大写）
def toUpperAll(text):
    return toLowAll(text).upper()
    
# 汉字转小写首字母
def toLowFirst(text):
    return ''.join(lazy_pinyin(text, style=Style.FIRST_LETTER))  
    
# 汉字转大写首字母
def toUpperFirst(text):
    return toLowFirst(text).upper()
    
if __name__ == "__main__":
    text = "中华人民共和国"
    print(toLowAll(text))
    print(toUpperAll(text))
    print(toLowFirst(text))
    print(toUpperFirst(text))
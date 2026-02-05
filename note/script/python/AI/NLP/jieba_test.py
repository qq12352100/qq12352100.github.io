# encoding=utf-8
'''
pip install -U jieba
'''
import jieba

def demonstrate_jieba_segmentation():
    """演示jieba分词的不同模式"""
    
    # 测试字符串列表
    test_strings = [
        "我来到北京清华大学",
        "乒乓球拍卖完了", 
        "中国科学技术大学",
        "他来到了网易杭研大厦",
        "小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
    ]
    
    print("=" * 50)
    print("jieba分词演示")
    print("=" * 50)
    
    # 演示不同分词模式
    for i, text in enumerate(test_strings, 1):
        print(f"\n示例 {i}: {text}")
        print("-" * 30)
        
        # Paddle模式（如果可用）
        try:
            seg_list = jieba.cut(text, use_paddle=True)
            print(f"Paddle模式: {'/'.join(seg_list)}")
        except Exception as e:
            print(f"Paddle模式: 不可用 ({e})")
        
        # 全模式
        seg_list = jieba.cut(text, cut_all=True)
        print(f"全模式: {'/'.join(seg_list)}")
        
        # 精确模式
        seg_list = jieba.cut(text, cut_all=False)
        print(f"精确模式: {'/'.join(seg_list)}")
        
        # 搜索引擎模式
        seg_list = jieba.cut_for_search(text)
        print(f"搜索引擎模式: {'/'.join(seg_list)}")

def compare_segmentation_modes():
    """对比不同模式的分词效果"""
    
    print("\n" + "=" * 50)
    print("分词模式对比")
    print("=" * 50)
    
    demo_text = "我来到北京清华大学"
    
    print(f"原文本: {demo_text}")
    print("-" * 30)
    
    # 全模式
    seg_full = jieba.cut(demo_text, cut_all=True)
    print(f"全模式: {'/'.join(seg_full)}")
    
    # 精确模式  
    seg_precise = jieba.cut(demo_text, cut_all=False)
    print(f"精确模式: {'/'.join(seg_precise)}")
    
    # 搜索引擎模式
    seg_search = jieba.cut_for_search(demo_text)
    print(f"搜索引擎模式: {'/'.join(seg_search)}")

if __name__ == "__main__":
    # 主演示
    demonstrate_jieba_segmentation()
    
    # 模式对比
    compare_segmentation_modes()
    
    print("\n" + "=" * 50)
    print("演示完成")
    print("=" * 50)
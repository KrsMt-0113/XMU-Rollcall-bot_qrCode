#!/usr/bin/env python3
"""
Interactive Hash Testing Tool
交互式哈希测试工具

这个脚本允许用户手动输入文本并立即查看其MD5哈希值，
方便进行交互式测试和验证。
"""

import hashlib
import sys

TARGET_HASH = "d89b99f96af9ff277008be738ca33795"

def calculate_hash(text, algorithm='md5'):
    """计算哈希值"""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
    }
    
    if algorithm in algorithms:
        return algorithms[algorithm](text.encode('utf-8')).hexdigest()
    return None

def display_hash_info(text):
    """显示哈希信息"""
    md5_hash = calculate_hash(text, 'md5')
    sha1_hash = calculate_hash(text, 'sha1')
    sha256_hash = calculate_hash(text, 'sha256')
    
    print("\n" + "=" * 80)
    print("哈希结果")
    print("=" * 80)
    print(f"输入文本: {repr(text)}")
    print(f"文本长度: {len(text)} 字符")
    print("-" * 80)
    print(f"MD5    : {md5_hash}")
    print(f"SHA1   : {sha1_hash}")
    print(f"SHA256 : {sha256_hash}")
    print("-" * 80)
    
    # 检查是否匹配目标哈希
    if md5_hash == TARGET_HASH:
        print("✓✓✓ MD5 匹配目标哈希! ✓✓✓")
        print("=" * 80)
        # 保存匹配结果
        with open('MATCH_FOUND.txt', 'w', encoding='utf-8') as f:
            f.write("找到匹配的哈希!\n")
            f.write("=" * 80 + "\n")
            f.write(f"输入文本: {text}\n")
            f.write(f"MD5哈希: {md5_hash}\n")
            f.write(f"目标哈希: {TARGET_HASH}\n")
        print("匹配结果已保存到 MATCH_FOUND.txt")
    else:
        print(f"目标MD5: {TARGET_HASH}")
        print("✗ 不匹配")
    
    print("=" * 80)

def interactive_mode():
    """交互模式"""
    print("=" * 80)
    print("交互式哈希测试工具")
    print("=" * 80)
    print(f"目标哈希: {TARGET_HASH}")
    print()
    print("输入文本来计算其哈希值")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'test' 运行快速测试")
    print("=" * 80)
    
    while True:
        try:
            user_input = input("\n请输入文本 > ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("退出程序")
                break
            
            if user_input.lower() == 'test':
                # 运行快速测试
                print("\n运行快速测试...")
                test_inputs = [
                    "78708",
                    "1763018727",
                    "230880",
                    "78708,1763018727,230880",
                    "787081763018727230880",
                ]
                for test_input in test_inputs:
                    display_hash_info(test_input)
            elif user_input:
                display_hash_info(user_input)
            else:
                print("请输入有效的文本")
                
        except KeyboardInterrupt:
            print("\n\n退出程序")
            break
        except Exception as e:
            print(f"错误: {e}")

def command_line_mode(text):
    """命令行模式"""
    display_hash_info(text)

def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        text = ' '.join(sys.argv[1:])
        command_line_mode(text)
    else:
        # 交互模式
        interactive_mode()

if __name__ == "__main__":
    main()

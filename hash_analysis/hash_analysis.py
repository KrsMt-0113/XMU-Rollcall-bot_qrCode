#!/usr/bin/env python3
"""
Hash Analysis Script
目标: 尝试重现哈希值 d89b99f96af9ff277008be738ca33795
已知明文可能包含: 78708, 1763018727, 230880
"""

import hashlib
import itertools

# 目标哈希值
TARGET_HASH = "d89b99f96af9ff277008be738ca33795"

# 已知的可能明文值
KNOWN_VALUES = ["78708", "1763018727", "230880"]

def calculate_md5(text):
    """计算MD5哈希值"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def calculate_sha1(text):
    """计算SHA1哈希值"""
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

def calculate_sha256(text):
    """计算SHA256哈希值"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def test_hash(text, algorithm='md5'):
    """测试给定文本的哈希值"""
    if algorithm == 'md5':
        result = calculate_md5(text)
    elif algorithm == 'sha1':
        result = calculate_sha1(text)
    elif algorithm == 'sha256':
        result = calculate_sha256(text)
    else:
        return None
    
    match = result == TARGET_HASH
    return result, match

def main():
    print("=" * 80)
    print("哈希分析工具")
    print("=" * 80)
    print(f"目标哈希: {TARGET_HASH}")
    print(f"哈希长度: {len(TARGET_HASH)} 字符 (可能是 MD5)")
    print(f"已知值: {KNOWN_VALUES}")
    print("=" * 80)
    
    results = []
    
    # 测试1: 单独的值
    print("\n[测试1] 单独的值")
    print("-" * 80)
    for val in KNOWN_VALUES:
        md5_hash, match = test_hash(val, 'md5')
        results.append({
            'input': val,
            'hash': md5_hash,
            'match': match
        })
        print(f"输入: {val:20s} | MD5: {md5_hash} | 匹配: {match}")
    
    # 测试2: 不同的组合顺序（无分隔符）
    print("\n[测试2] 值的组合（无分隔符）")
    print("-" * 80)
    for perm in itertools.permutations(KNOWN_VALUES):
        text = ''.join(perm)
        md5_hash, match = test_hash(text, 'md5')
        results.append({
            'input': text,
            'hash': md5_hash,
            'match': match
        })
        print(f"输入: {text:30s} | MD5: {md5_hash} | 匹配: {match}")
        if match:
            print(f"✓✓✓ 找到匹配! 输入: {text}")
    
    # 测试3: 用逗号分隔的组合
    print("\n[测试3] 值的组合（逗号分隔）")
    print("-" * 80)
    for perm in itertools.permutations(KNOWN_VALUES):
        text = ','.join(perm)
        md5_hash, match = test_hash(text, 'md5')
        results.append({
            'input': text,
            'hash': md5_hash,
            'match': match
        })
        print(f"输入: {text:30s} | MD5: {md5_hash} | 匹配: {match}")
        if match:
            print(f"✓✓✓ 找到匹配! 输入: {text}")
    
    # 测试4: 用空格分隔的组合
    print("\n[测试4] 值的组合（空格分隔）")
    print("-" * 80)
    for perm in itertools.permutations(KNOWN_VALUES):
        text = ' '.join(perm)
        md5_hash, match = test_hash(text, 'md5')
        results.append({
            'input': text,
            'hash': md5_hash,
            'match': match
        })
        print(f"输入: {text:30s} | MD5: {md5_hash} | 匹配: {match}")
        if match:
            print(f"✓✓✓ 找到匹配! 输入: {text}")
    
    # 测试5: 用下划线分隔的组合
    print("\n[测试5] 值的组合（下划线分隔）")
    print("-" * 80)
    for perm in itertools.permutations(KNOWN_VALUES):
        text = '_'.join(perm)
        md5_hash, match = test_hash(text, 'md5')
        results.append({
            'input': text,
            'hash': md5_hash,
            'match': match
        })
        print(f"输入: {text:30s} | MD5: {md5_hash} | 匹配: {match}")
        if match:
            print(f"✓✓✓ 找到匹配! 输入: {text}")
    
    # 测试6: 两个值的组合
    print("\n[测试6] 两个值的组合（各种分隔符）")
    print("-" * 80)
    separators = ['', ',', ' ', '_', '-', '|', ':', ';']
    for combo in itertools.combinations(KNOWN_VALUES, 2):
        for perm in itertools.permutations(combo):
            for sep in separators:
                text = sep.join(perm)
                md5_hash, match = test_hash(text, 'md5')
                results.append({
                    'input': text,
                    'hash': md5_hash,
                    'match': match
                })
                if match:
                    print(f"✓✓✓ 找到匹配! 输入: {text} | MD5: {md5_hash}")
    
    # 测试7: 整数形式（转换为字符串）
    print("\n[测试7] 整数值的数学运算")
    print("-" * 80)
    nums = [int(v) for v in KNOWN_VALUES]
    operations = [
        (sum(nums), f"sum({KNOWN_VALUES})"),
        (nums[0] + nums[1], f"{nums[0]} + {nums[1]}"),
        (nums[0] + nums[2], f"{nums[0]} + {nums[2]}"),
        (nums[1] + nums[2], f"{nums[1]} + {nums[2]}"),
        (nums[0] * nums[1], f"{nums[0]} * {nums[1]}"),
        (nums[0] * nums[2], f"{nums[0]} * {nums[2]}"),
        (nums[1] * nums[2], f"{nums[1]} * {nums[2]}"),
    ]
    
    for result_val, desc in operations:
        text = str(result_val)
        md5_hash, match = test_hash(text, 'md5')
        results.append({
            'input': text,
            'hash': md5_hash,
            'match': match
        })
        print(f"输入: {text:30s} ({desc}) | MD5: {md5_hash} | 匹配: {match}")
        if match:
            print(f"✓✓✓ 找到匹配! 输入: {text} ({desc})")
    
    # 输出总结
    print("\n" + "=" * 80)
    print("分析总结")
    print("=" * 80)
    matched = [r for r in results if r['match']]
    if matched:
        print(f"找到 {len(matched)} 个匹配的哈希值:")
        for m in matched:
            print(f"  - 输入: {m['input']}")
            print(f"    哈希: {m['hash']}")
    else:
        print("未找到匹配的哈希值")
        print("\n建议:")
        print("1. 可能需要更多的明文值")
        print("2. 可能使用了不同的哈希算法")
        print("3. 可能在哈希前对数据进行了额外的处理")
        print("4. 可能包含了其他未知的字符或格式")
    
    # 保存结果到文件
    with open('hash_analysis_results.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("哈希分析结果\n")
        f.write("=" * 80 + "\n")
        f.write(f"目标哈希: {TARGET_HASH}\n")
        f.write(f"已知值: {KNOWN_VALUES}\n")
        f.write(f"总测试数: {len(results)}\n")
        f.write(f"匹配数: {len(matched)}\n")
        f.write("=" * 80 + "\n\n")
        
        if matched:
            f.write("匹配的结果:\n")
            f.write("-" * 80 + "\n")
            for m in matched:
                f.write(f"输入: {m['input']}\n")
                f.write(f"哈希: {m['hash']}\n\n")
        else:
            f.write("未找到匹配的哈希值\n")
        
        f.write("\n所有测试结果:\n")
        f.write("-" * 80 + "\n")
        for r in results:
            f.write(f"输入: {r['input']:40s} | 哈希: {r['hash']} | 匹配: {r['match']}\n")
    
    print(f"\n结果已保存到 hash_analysis_results.txt")
    print("=" * 80)

if __name__ == "__main__":
    main()

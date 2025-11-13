#!/usr/bin/env python3
"""
Extended Hash Analysis Script
扩展的哈希分析脚本 - 测试更多组合和格式
"""

import hashlib
import itertools

# 目标哈希值
TARGET_HASH = "d89b99f96af9ff277008be738ca33795"

# 已知的可能明文值
KNOWN_VALUES = ["78708", "1763018727", "230880"]

def calculate_hash(text, algorithm='md5'):
    """计算哈希值"""
    hash_funcs = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
    }
    
    if algorithm in hash_funcs:
        return hash_funcs[algorithm](text.encode('utf-8')).hexdigest()
    return None

def test_combinations():
    """测试更多的组合"""
    print("=" * 80)
    print("扩展哈希分析")
    print("=" * 80)
    print(f"目标哈希: {TARGET_HASH}")
    print(f"已知值: {KNOWN_VALUES}")
    print("=" * 80)
    
    results = []
    found = False
    
    # 测试不同的格式
    test_cases = []
    
    # 1. JSON格式
    test_cases.append(f'{{"courseId":{KNOWN_VALUES[0]},"activityId":{KNOWN_VALUES[1]},"data":{KNOWN_VALUES[2]}}}')
    test_cases.append(f'{{"data":{KNOWN_VALUES[2]},"courseId":{KNOWN_VALUES[0]},"activityId":{KNOWN_VALUES[1]}}}')
    
    # 2. URL参数格式
    for perm in itertools.permutations(zip(['courseId', 'activityId', 'data'], KNOWN_VALUES)):
        test_cases.append('&'.join([f'{k}={v}' for k, v in perm]))
        test_cases.append('?'+'&'.join([f'{k}={v}' for k, v in perm]))
    
    # 3. 带键值对的格式
    for sep1 in [':', '=']:
        for sep2 in [',', ';', '&', '|']:
            for perm in itertools.permutations(zip(['courseId', 'activityId', 'data'], KNOWN_VALUES)):
                test_cases.append(sep2.join([f'{k}{sep1}{v}' for k, v in perm]))
    
    # 4. 原始值的各种排列和连接
    for num_values in range(1, 4):
        for combo in itertools.combinations(KNOWN_VALUES, num_values):
            for perm in itertools.permutations(combo):
                for sep in ['', ',', ' ', '_', '-', '|', ':', ';', '/', '.', '\t', '\n']:
                    test_cases.append(sep.join(perm))
    
    # 5. 带引号的格式
    for perm in itertools.permutations(KNOWN_VALUES):
        test_cases.append(','.join([f'"{v}"' for v in perm]))
        test_cases.append(','.join([f"'{v}'" for v in perm]))
    
    # 6. 数组格式
    for perm in itertools.permutations(KNOWN_VALUES):
        test_cases.append('[' + ','.join(perm) + ']')
        test_cases.append('[' + ','.join([f'"{v}"' for v in perm]) + ']')
    
    # 7. 带前缀/后缀
    for val in KNOWN_VALUES:
        for prefix in ['', 'data=', 'value=', 'id=', 'code=']:
            for suffix in ['', '&', ';']:
                test_cases.append(f'{prefix}{val}{suffix}')
    
    # 8. 整数值
    for val in KNOWN_VALUES:
        # 去掉前导零
        test_cases.append(str(int(val)))
    
    # 9. 十六进制格式
    for val in KNOWN_VALUES:
        test_cases.append(hex(int(val)))
        test_cases.append(hex(int(val))[2:])  # 去掉'0x'
    
    print(f"\n总共生成了 {len(test_cases)} 个测试用例")
    print("开始测试...\n")
    
    # 去重
    test_cases = list(set(test_cases))
    print(f"去重后: {len(test_cases)} 个测试用例\n")
    
    # 测试所有用例
    for i, text in enumerate(test_cases):
        md5_hash = calculate_hash(text, 'md5')
        
        if md5_hash == TARGET_HASH:
            print("=" * 80)
            print(f"✓✓✓ 找到匹配! ✓✓✓")
            print("=" * 80)
            print(f"输入文本: {text}")
            print(f"MD5哈希: {md5_hash}")
            print("=" * 80)
            results.append({
                'input': text,
                'hash': md5_hash,
                'match': True
            })
            found = True
        
        if (i + 1) % 100 == 0:
            print(f"已测试 {i + 1}/{len(test_cases)} 个用例...")
    
    if not found:
        print("\n未在预设组合中找到匹配")
        print("尝试暴力测试一些特殊格式...\n")
        
        # 额外测试：特殊编码
        special_tests = []
        
        # Base64编码
        import base64
        for val in KNOWN_VALUES:
            special_tests.append(base64.b64encode(val.encode()).decode())
        
        # URL编码
        import urllib.parse
        for val in KNOWN_VALUES:
            special_tests.append(urllib.parse.quote(val))
        
        # 反转
        for val in KNOWN_VALUES:
            special_tests.append(val[::-1])
        
        # 测试特殊格式
        for text in special_tests:
            md5_hash = calculate_hash(text, 'md5')
            if md5_hash == TARGET_HASH:
                print("=" * 80)
                print(f"✓✓✓ 在特殊格式中找到匹配! ✓✓✓")
                print("=" * 80)
                print(f"输入文本: {text}")
                print(f"MD5哈希: {md5_hash}")
                print("=" * 80)
                found = True
    
    # 保存详细结果
    with open('extended_analysis_results.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("扩展哈希分析结果\n")
        f.write("=" * 80 + "\n")
        f.write(f"目标哈希: {TARGET_HASH}\n")
        f.write(f"已知值: {KNOWN_VALUES}\n")
        f.write(f"测试用例数: {len(test_cases)}\n")
        f.write("=" * 80 + "\n\n")
        
        if found:
            f.write("找到匹配的结果:\n")
            f.write("-" * 80 + "\n")
            for r in results:
                if r['match']:
                    f.write(f"输入: {r['input']}\n")
                    f.write(f"哈希: {r['hash']}\n\n")
        else:
            f.write("未找到匹配的哈希值\n\n")
            f.write("建议:\n")
            f.write("1. 可能存在其他未知的明文值\n")
            f.write("2. 可能使用了加盐(salt)处理\n")
            f.write("3. 可能进行了多次哈希运算\n")
            f.write("4. 可能使用了自定义的编码方式\n")
    
    print(f"\n结果已保存到 extended_analysis_results.txt")
    return found

if __name__ == "__main__":
    found = test_combinations()
    if not found:
        print("\n" + "=" * 80)
        print("总结")
        print("=" * 80)
        print("未能找到匹配的哈希值。")
        print("这表明可能:")
        print("1. 明文中包含其他未知的数据")
        print("2. 使用了加盐(salt)或密钥")
        print("3. 进行了多层哈希或其他加密处理")
        print("4. 使用了非标准的编码格式")
        print("=" * 80)

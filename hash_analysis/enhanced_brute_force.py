#!/usr/bin/env python3
"""
Enhanced Brute Force Hash Analysis
增强暴力哈希分析 - 包含新的可能明文值

新增可能的明文: courseId, data, rollcallId
测试不同的排列组合，不一定包含所有明文值
"""

import hashlib
import itertools

TARGET_HASH = "d89b99f96af9ff277008be738ca33795"

# 已知的数值
KNOWN_VALUES = ["78708", "1763018727", "230880"]

# 新增的可能字段名
FIELD_NAMES = ["courseId", "data", "rollcallId"]

# 所有可能的值（数值 + 字段名）
ALL_VALUES = KNOWN_VALUES + FIELD_NAMES

def md5(text):
    """计算MD5"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def test_and_report(text, description=""):
    """测试文本并报告结果"""
    h = md5(text)
    if h == TARGET_HASH:
        print("=" * 80)
        print(f"✓✓✓ 找到匹配! ✓✓✓")
        print("=" * 80)
        print(f"描述: {description}")
        print(f"输入: {text}")
        print(f"MD5: {h}")
        print("=" * 80)
        
        # 保存到文件
        with open('MATCH_FOUND.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("找到匹配的哈希!\n")
            f.write("=" * 80 + "\n")
            f.write(f"描述: {description}\n")
            f.write(f"输入文本: {text}\n")
            f.write(f"MD5哈希: {h}\n")
            f.write(f"目标哈希: {TARGET_HASH}\n")
            f.write("=" * 80 + "\n")
        
        return True
    return False

def test_all_combinations():
    """测试所有可能的组合"""
    print("=" * 80)
    print("增强暴力哈希分析")
    print("=" * 80)
    print(f"目标哈希: {TARGET_HASH}")
    print(f"数值: {KNOWN_VALUES}")
    print(f"字段名: {FIELD_NAMES}")
    print("=" * 80)
    
    total_tests = 0
    found = False
    
    # 测试1: 单独的值（数值和字段名）
    print("\n[测试1] 单独的值")
    print("-" * 80)
    for val in ALL_VALUES:
        total_tests += 1
        if test_and_report(val, f"单独值: {val}"):
            found = True
    print(f"测试了 {len(ALL_VALUES)} 个单独值")
    
    # 测试2: 两个值的组合（所有可能的分隔符）
    print("\n[测试2] 两个值的组合")
    print("-" * 80)
    separators = ['', ',', ' ', '_', '-', ':', '=', '&', '|', ';', '/', '.', '~', '!']
    
    for combo in itertools.combinations(ALL_VALUES, 2):
        for perm in itertools.permutations(combo):
            for sep in separators:
                text = sep.join(perm)
                total_tests += 1
                if test_and_report(text, f"两值组合: {perm[0]} {sep} {perm[1]}"):
                    found = True
    
    print(f"测试了两值组合")
    
    # 测试3: 三个值的组合
    print("\n[测试3] 三个值的组合")
    print("-" * 80)
    
    for combo in itertools.combinations(ALL_VALUES, 3):
        for perm in itertools.permutations(combo):
            for sep in separators:
                text = sep.join(perm)
                total_tests += 1
                if test_and_report(text, f"三值组合: {sep.join(perm)}"):
                    found = True
    
    print(f"测试了三值组合")
    
    # 测试4: 键值对格式 (key=value)
    print("\n[测试4] 键值对格式")
    print("-" * 80)
    
    # 字段名作为键，数值作为值
    for field in FIELD_NAMES:
        for value in KNOWN_VALUES:
            for kv_sep in ['=', ':']:
                text = f"{field}{kv_sep}{value}"
                total_tests += 1
                if test_and_report(text, f"键值对: {field}{kv_sep}{value}"):
                    found = True
    
    # 多个键值对的组合
    for sep in ['&', ',', ';', ' ', '|']:
        # courseId=78708&data=1763018727
        for field_perm in itertools.permutations(FIELD_NAMES):
            for value_perm in itertools.permutations(KNOWN_VALUES):
                if len(field_perm) == len(value_perm):
                    pairs = [f"{k}={v}" for k, v in zip(field_perm, value_perm)]
                    text = sep.join(pairs)
                    total_tests += 1
                    if test_and_report(text, f"多键值对: {text}"):
                        found = True
                    
                    # 也尝试用冒号
                    pairs = [f"{k}:{v}" for k, v in zip(field_perm, value_perm)]
                    text = sep.join(pairs)
                    total_tests += 1
                    if test_and_report(text, f"多键值对(冒号): {text}"):
                        found = True
    
    print(f"测试了键值对格式")
    
    # 测试5: 只用数值的组合（不包含字段名）
    print("\n[测试5] 只用数值的各种组合")
    print("-" * 80)
    
    # 单个数值
    for val in KNOWN_VALUES:
        total_tests += 1
        if test_and_report(val, f"单个数值: {val}"):
            found = True
    
    # 两个数值
    for combo in itertools.combinations(KNOWN_VALUES, 2):
        for perm in itertools.permutations(combo):
            for sep in separators:
                text = sep.join(perm)
                total_tests += 1
                if test_and_report(text, f"两数值: {perm[0]}{sep}{perm[1]}"):
                    found = True
    
    # 三个数值
    for perm in itertools.permutations(KNOWN_VALUES):
        for sep in separators:
            text = sep.join(perm)
            total_tests += 1
            if test_and_report(text, f"三数值: {sep.join(perm)}"):
                found = True
    
    print(f"测试了数值组合")
    
    # 测试6: 只用字段名的组合
    print("\n[测试6] 只用字段名的组合")
    print("-" * 80)
    
    for combo_size in range(1, len(FIELD_NAMES) + 1):
        for combo in itertools.combinations(FIELD_NAMES, combo_size):
            for perm in itertools.permutations(combo):
                for sep in separators:
                    text = sep.join(perm)
                    total_tests += 1
                    if test_and_report(text, f"字段名组合: {sep.join(perm)}"):
                        found = True
    
    print(f"测试了字段名组合")
    
    # 测试7: JSON格式
    print("\n[测试7] JSON格式")
    print("-" * 80)
    
    for field_perm in itertools.permutations(FIELD_NAMES):
        for value_perm in itertools.permutations(KNOWN_VALUES):
            if len(field_perm) == len(value_perm):
                # 不带引号
                pairs = [f'"{k}":{v}' for k, v in zip(field_perm, value_perm)]
                text = '{' + ','.join(pairs) + '}'
                total_tests += 1
                if test_and_report(text, f"JSON格式: {text}"):
                    found = True
                
                # 带引号
                pairs = [f'"{k}":"{v}"' for k, v in zip(field_perm, value_perm)]
                text = '{' + ','.join(pairs) + '}'
                total_tests += 1
                if test_and_report(text, f"JSON格式(带引号): {text}"):
                    found = True
    
    print(f"测试了JSON格式")
    
    # 测试8: 部分组合（不是所有值）
    print("\n[测试8] 数值+字段名的混合组合")
    print("-" * 80)
    
    # 一个数值 + 一个字段名
    for val in KNOWN_VALUES:
        for field in FIELD_NAMES:
            for sep in separators:
                # 数值在前
                text = f"{val}{sep}{field}"
                total_tests += 1
                if test_and_report(text, f"数值+字段: {val}{sep}{field}"):
                    found = True
                
                # 字段名在前
                text = f"{field}{sep}{val}"
                total_tests += 1
                if test_and_report(text, f"字段+数值: {field}{sep}{val}"):
                    found = True
    
    # 两个数值 + 一个字段名
    for val_combo in itertools.combinations(KNOWN_VALUES, 2):
        for field in FIELD_NAMES:
            for sep in separators:
                # 尝试不同的位置
                items = list(val_combo) + [field]
                for perm in itertools.permutations(items):
                    text = sep.join(perm)
                    total_tests += 1
                    if test_and_report(text, f"2数值+1字段: {sep.join(perm)}"):
                        found = True
    
    print(f"测试了混合组合")
    
    # 测试9: URL格式
    print("\n[测试9] URL参数格式")
    print("-" * 80)
    
    for field_perm in itertools.permutations(FIELD_NAMES):
        for value_perm in itertools.permutations(KNOWN_VALUES):
            if len(field_perm) == len(value_perm):
                pairs = [f"{k}={v}" for k, v in zip(field_perm, value_perm)]
                text = '&'.join(pairs)
                total_tests += 1
                if test_and_report(text, f"URL参数: {text}"):
                    found = True
                
                # 带问号
                text = '?' + '&'.join(pairs)
                total_tests += 1
                if test_and_report(text, f"URL参数(带?): {text}"):
                    found = True
    
    print(f"测试了URL格式")
    
    # 测试10: 加盐测试
    print("\n[测试10] 加盐测试")
    print("-" * 80)
    
    common_salts = ['', 'xmu', 'rollcall', 'qrcode', 'tronclass', 'secret', 'key', 'salt']
    
    # 对每个值加盐
    for val in ALL_VALUES:
        for salt in common_salts:
            if salt:  # 空字符串已经在单独值中测试过了
                # 盐在前
                text = salt + val
                total_tests += 1
                if test_and_report(text, f"盐在前: {salt}+{val}"):
                    found = True
                
                # 盐在后
                text = val + salt
                total_tests += 1
                if test_and_report(text, f"盐在后: {val}+{salt}"):
                    found = True
    
    # 对组合值加盐
    for sep in ['', ',', '_']:
        for combo in itertools.combinations(KNOWN_VALUES, 2):
            combined = sep.join(combo)
            for salt in common_salts:
                if salt:
                    text = salt + combined
                    total_tests += 1
                    if test_and_report(text, f"组合加盐(前): {salt}+{combined}"):
                        found = True
                    
                    text = combined + salt
                    total_tests += 1
                    if test_and_report(text, f"组合加盐(后): {combined}+{salt}"):
                        found = True
    
    print(f"测试了加盐情况")
    
    # 总结
    print("\n" + "=" * 80)
    print("增强暴力分析总结")
    print("=" * 80)
    print(f"总测试数: {total_tests}")
    print(f"目标哈希: {TARGET_HASH}")
    
    if found:
        print("\n✓✓✓ 找到匹配! 详见上方输出和 MATCH_FOUND.txt 文件")
    else:
        print("\n✗ 未找到匹配的哈希值")
        print("\n可能的原因:")
        print("1. 需要更多的明文值或不同的组合方式")
        print("2. 使用了更复杂的盐值或密钥")
        print("3. 数据经过了特殊的编码或预处理")
        print("4. 使用了自定义的哈希算法或多重哈希")
    
    print("=" * 80)
    
    # 保存结果
    with open('enhanced_brute_force_results.txt', 'w', encoding='utf-8') as f:
        f.write("增强暴力哈希分析结果\n")
        f.write("=" * 80 + "\n")
        f.write(f"目标哈希: {TARGET_HASH}\n")
        f.write(f"已知数值: {KNOWN_VALUES}\n")
        f.write(f"可能字段名: {FIELD_NAMES}\n")
        f.write(f"总测试数: {total_tests}\n")
        f.write(f"结果: {'找到匹配' if found else '未找到匹配'}\n")
        f.write("=" * 80 + "\n")
    
    return found

if __name__ == "__main__":
    found = test_all_combinations()
    if found:
        print("\n结果已保存到 MATCH_FOUND.txt")
    print("详细结果已保存到 enhanced_brute_force_results.txt")

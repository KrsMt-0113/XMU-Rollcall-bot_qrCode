#!/usr/bin/env python3
"""
Comprehensive Hash Analysis
综合哈希分析 - 测试所有可能的组合模式

包含字段名和数值的所有可能组合
"""

import hashlib
import itertools

TARGET_HASH = "d89b99f96af9ff277008be738ca33795"

# 数值
KNOWN_VALUES = ["78708", "1763018727", "230880"]

# 字段名
FIELD_NAMES = ["courseId", "data", "rollcallId"]

def md5(text):
    """计算MD5"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def test_hash(text):
    """测试并返回是否匹配"""
    h = md5(text)
    if h == TARGET_HASH:
        print("\n" + "=" * 80)
        print("✓✓✓ 找到匹配! ✓✓✓")
        print("=" * 80)
        print(f"输入文本: {text}")
        print(f"MD5哈希: {h}")
        print("=" * 80)
        
        with open('MATCH_FOUND.txt', 'w', encoding='utf-8') as f:
            f.write("找到匹配!\n")
            f.write("=" * 80 + "\n")
            f.write(f"输入: {text}\n")
            f.write(f"MD5: {h}\n")
            f.write(f"目标: {TARGET_HASH}\n")
        
        return True
    return False

def main():
    print("=" * 80)
    print("综合哈希分析")
    print("=" * 80)
    print(f"目标: {TARGET_HASH}")
    print(f"数值: {KNOWN_VALUES}")
    print(f"字段: {FIELD_NAMES}")
    print("=" * 80)
    
    total = 0
    found = False
    
    # 所有分隔符
    seps = ['', ',', ' ', '_', '-', ':', '=', '&', '|', ';', '/', '.', '~', '!', '\t', '\n']
    
    print("\n正在测试各种组合...")
    
    # 1. 测试所有可能的字段名和数值的映射
    print("\n[1] 字段名=数值 的所有映射")
    for field_indices in itertools.permutations(range(len(FIELD_NAMES))):
        for value_indices in itertools.permutations(range(len(KNOWN_VALUES))):
            # 创建映射
            mapping = {}
            for i, field_idx in enumerate(field_indices):
                if i < len(value_indices):
                    mapping[FIELD_NAMES[field_idx]] = KNOWN_VALUES[value_indices[i]]
            
            # 测试不同的格式
            for sep1 in ['=', ':']:
                for sep2 in ['&', ',', ';', ' ', '|', '']:
                    # courseId=78708&data=1763018727
                    if sep2:
                        pairs = [f"{k}{sep1}{v}" for k, v in mapping.items()]
                        text = sep2.join(pairs)
                    else:
                        # 无分隔符: courseId=78708data=1763018727
                        text = ''.join([f"{k}{sep1}{v}" for k, v in mapping.items()])
                    
                    total += 1
                    if test_hash(text):
                        found = True
                        return True
    
    print(f"   测试了 {total} 种组合")
    
    # 2. 测试只有值的不同排列（不同数量）
    print("\n[2] 仅数值的所有子集排列")
    for r in range(1, len(KNOWN_VALUES) + 1):
        for combo in itertools.combinations(KNOWN_VALUES, r):
            for perm in itertools.permutations(combo):
                for sep in seps:
                    text = sep.join(perm)
                    total += 1
                    if test_hash(text):
                        found = True
                        return True
    
    print(f"   总计测试 {total} 种")
    
    # 3. 测试只有字段名的组合
    print("\n[3] 仅字段名的所有子集排列")
    for r in range(1, len(FIELD_NAMES) + 1):
        for combo in itertools.combinations(FIELD_NAMES, r):
            for perm in itertools.permutations(combo):
                for sep in seps:
                    text = sep.join(perm)
                    total += 1
                    if test_hash(text):
                        found = True
                        return True
    
    print(f"   总计测试 {total} 种")
    
    # 4. 测试字段名和数值的混合（任意组合）
    print("\n[4] 字段名和数值的混合排列")
    all_items = KNOWN_VALUES + FIELD_NAMES
    for r in range(1, len(all_items) + 1):
        for combo in itertools.combinations(all_items, r):
            for perm in itertools.permutations(combo):
                for sep in seps[:8]:  # 限制分隔符数量以节省时间
                    text = sep.join(perm)
                    total += 1
                    if test_hash(text):
                        found = True
                        return True
                    
                    if total % 1000 == 0:
                        print(f"   已测试 {total} 种组合...")
    
    print(f"   总计测试 {total} 种")
    
    # 5. 测试特定的键值对格式
    print("\n[5] 特定键值对格式")
    # 可能的键值对组合
    for field in FIELD_NAMES:
        for value in KNOWN_VALUES:
            # 单个键值对
            for kv_sep in ['=', ':']:
                text = f"{field}{kv_sep}{value}"
                total += 1
                if test_hash(text):
                    found = True
                    return True
            
            # 带引号
            for kv_sep in ['=', ':']:
                text = f'"{field}"{kv_sep}"{value}"'
                total += 1
                if test_hash(text):
                    found = True
                    return True
    
    # 多个键值对
    for num_pairs in range(1, 4):
        for field_combo in itertools.combinations(FIELD_NAMES, num_pairs):
            for value_combo in itertools.combinations(KNOWN_VALUES, num_pairs):
                for field_perm in itertools.permutations(field_combo):
                    for value_perm in itertools.permutations(value_combo):
                        for kv_sep in ['=', ':']:
                            for pair_sep in ['&', ',', ';', ' ', '']:
                                pairs = [f"{k}{kv_sep}{v}" for k, v in zip(field_perm, value_perm)]
                                if pair_sep:
                                    text = pair_sep.join(pairs)
                                else:
                                    text = ''.join(pairs)
                                total += 1
                                if test_hash(text):
                                    found = True
                                    return True
    
    print(f"   总计测试 {total} 种")
    
    # 6. JSON格式的各种变体
    print("\n[6] JSON格式变体")
    for num_pairs in range(1, 4):
        for field_combo in itertools.combinations(FIELD_NAMES, num_pairs):
            for value_combo in itertools.combinations(KNOWN_VALUES, num_pairs):
                for field_perm in itertools.permutations(field_combo):
                    for value_perm in itertools.permutations(value_combo):
                        # 不带引号的值
                        pairs = [f'"{k}":{v}' for k, v in zip(field_perm, value_perm)]
                        text = '{' + ','.join(pairs) + '}'
                        total += 1
                        if test_hash(text):
                            found = True
                            return True
                        
                        # 带引号的值
                        pairs = [f'"{k}":"{v}"' for k, v in zip(field_perm, value_perm)]
                        text = '{' + ','.join(pairs) + '}'
                        total += 1
                        if test_hash(text):
                            found = True
                            return True
                        
                        # 不带外层大括号
                        pairs = [f'"{k}":"{v}"' for k, v in zip(field_perm, value_perm)]
                        text = ','.join(pairs)
                        total += 1
                        if test_hash(text):
                            found = True
                            return True
    
    print(f"   总计测试 {total} 种")
    
    # 7. 加盐测试
    print("\n[7] 加盐测试")
    salts = ['xmu', 'rollcall', 'qrcode', 'tronclass', 'secret', 'key', 'salt', 'token']
    
    # 对单个值加盐
    for item in KNOWN_VALUES + FIELD_NAMES:
        for salt in salts:
            # 盐在前
            text = salt + item
            total += 1
            if test_hash(text):
                found = True
                return True
            
            # 盐在后
            text = item + salt
            total += 1
            if test_hash(text):
                found = True
                return True
    
    # 对组合值加盐
    for sep in ['', ',', '_', '&']:
        for combo in itertools.combinations(KNOWN_VALUES, 2):
            combined = sep.join(combo)
            for salt in salts:
                text = salt + combined
                total += 1
                if test_hash(text):
                    found = True
                    return True
                
                text = combined + salt
                total += 1
                if test_hash(text):
                    found = True
                    return True
    
    print(f"   总计测试 {total} 种")
    
    # 8. 特殊格式
    print("\n[8] 特殊格式")
    # URL格式
    for num_pairs in range(1, 4):
        for field_combo in itertools.combinations(FIELD_NAMES, num_pairs):
            for value_combo in itertools.combinations(KNOWN_VALUES, num_pairs):
                for field_perm in itertools.permutations(field_combo):
                    for value_perm in itertools.permutations(value_combo):
                        pairs = [f"{k}={v}" for k, v in zip(field_perm, value_perm)]
                        
                        # 不带?
                        text = '&'.join(pairs)
                        total += 1
                        if test_hash(text):
                            found = True
                            return True
                        
                        # 带?
                        text = '?' + '&'.join(pairs)
                        total += 1
                        if test_hash(text):
                            found = True
                            return True
    
    print(f"   总计测试 {total} 种")
    
    # 总结
    print("\n" + "=" * 80)
    print("分析完成")
    print("=" * 80)
    print(f"总测试数: {total}")
    
    if found:
        print("✓ 找到匹配!")
    else:
        print("✗ 未找到匹配")
    
    print("=" * 80)
    
    # 保存结果
    with open('comprehensive_results.txt', 'w', encoding='utf-8') as f:
        f.write(f"综合分析结果\n")
        f.write("=" * 80 + "\n")
        f.write(f"目标哈希: {TARGET_HASH}\n")
        f.write(f"总测试数: {total}\n")
        f.write(f"结果: {'找到' if found else '未找到'}\n")
    
    return found

if __name__ == "__main__":
    found = main()
    if found:
        print("\n✓ 结果已保存到 MATCH_FOUND.txt")
    else:
        print("\n详细结果已保存到 comprehensive_results.txt")

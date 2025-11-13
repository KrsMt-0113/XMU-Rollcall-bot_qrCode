#!/usr/bin/env python3
"""
Additional Pattern Testing
额外模式测试 - 测试一些特殊的组合模式
"""

import hashlib
import itertools

TARGET_HASH = "d89b99f96af9ff277008be738ca33795"
KNOWN_VALUES = ["78708", "1763018727", "230880"]
FIELD_NAMES = ["courseId", "data", "rollcallId"]

def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def test_and_log(text, desc=""):
    h = md5(text)
    if h == TARGET_HASH:
        msg = f"\n{'='*80}\n✓✓✓ 找到匹配! ✓✓✓\n{'='*80}\n"
        msg += f"描述: {desc}\n输入: {text}\nMD5: {h}\n{'='*80}\n"
        print(msg)
        with open('MATCH_FOUND.txt', 'w') as f:
            f.write(msg)
        return True
    return False

def main():
    print("="*80)
    print("额外模式测试")
    print("="*80)
    print(f"目标: {TARGET_HASH}\n")
    
    total = 0
    
    # 1. 测试字段名和值直接连接（无分隔符）
    print("[1] 字段名+值直接连接")
    for field in FIELD_NAMES:
        for value in KNOWN_VALUES:
            # field+value
            total += 1
            if test_and_log(field + value, f"{field}+{value}"):
                return True
            
            # value+field
            total += 1
            if test_and_log(value + field, f"{value}+{field}"):
                return True
    
    # 2. 测试特殊的键值对格式
    print("[2] 特殊键值对格式")
    for f1, v1 in itertools.product(FIELD_NAMES, KNOWN_VALUES):
        for f2, v2 in itertools.product(FIELD_NAMES, KNOWN_VALUES):
            if f1 != f2:
                # field1:value1,field2:value2
                text = f"{f1}:{v1},{f2}:{v2}"
                total += 1
                if test_and_log(text, "两键值对(冒号逗号)"):
                    return True
                
                # field1=value1&field2=value2
                text = f"{f1}={v1}&{f2}={v2}"
                total += 1
                if test_and_log(text, "两键值对(等号&)"):
                    return True
    
    # 3. 测试数值在前，字段在后的组合
    print("[3] 数值+字段组合")
    for v1, v2 in itertools.combinations(KNOWN_VALUES, 2):
        for field in FIELD_NAMES:
            for sep in ['', ',', '_', ' ']:
                # v1,v2,field
                text = sep.join([v1, v2, field])
                total += 1
                if test_and_log(text, f"{v1},{v2},{field}"):
                    return True
                
                # v1,field,v2
                text = sep.join([v1, field, v2])
                total += 1
                if test_and_log(text, f"{v1},{field},{v2}"):
                    return True
    
    # 4. 测试包含特定格式的字符串
    print("[4] 包含特定关键字的格式")
    keywords = ['qr', 'code', 'hash', 'sign', 'answer']
    for keyword in keywords:
        for value in KNOWN_VALUES:
            for sep in ['', '_', '-', ':']:
                # keyword+value
                text = keyword + sep + value
                total += 1
                if test_and_log(text, f"{keyword}{sep}{value}"):
                    return True
                
                # value+keyword
                text = value + sep + keyword
                total += 1
                if test_and_log(text, f"{value}{sep}{keyword}"):
                    return True
    
    # 5. 测试数值的不同表示
    print("[5] 数值的不同表示")
    for val_str in KNOWN_VALUES:
        val_int = int(val_str)
        
        # 十六进制（小写）
        hex_val = hex(val_int)[2:]
        total += 1
        if test_and_log(hex_val, f"十六进制: {hex_val}"):
            return True
        
        # 十六进制（大写）
        hex_val_upper = hex(val_int)[2:].upper()
        total += 1
        if test_and_log(hex_val_upper, f"十六进制大写: {hex_val_upper}"):
            return True
    
    # 6. 测试字段名的变体
    print("[6] 字段名变体")
    field_variations = {
        'courseId': ['courseid', 'CourseId', 'COURSEID', 'course_id', 'course-id'],
        'data': ['Data', 'DATA'],
        'rollcallId': ['rollcallid', 'RollcallId', 'ROLLCALLID', 'rollcall_id', 'rollcall-id']
    }
    
    for original_field in FIELD_NAMES:
        if original_field in field_variations:
            for variant in field_variations[original_field]:
                for value in KNOWN_VALUES:
                    # variant=value
                    text = f"{variant}={value}"
                    total += 1
                    if test_and_log(text, f"字段变体: {variant}={value}"):
                        return True
    
    # 7. 测试特定的三元组
    print("[7] 特定的三元组组合")
    # courseId, rollcallId, data 对应 78708, 1763018727, 230880
    mappings = [
        ('courseId', '78708'),
        ('rollcallId', '1763018727'),
        ('data', '230880'),
    ]
    
    for perm in itertools.permutations(mappings):
        for kv_sep in ['=', ':']:
            for pair_sep in ['&', ',', ';', ' ', '']:
                pairs = [f"{k}{kv_sep}{v}" for k, v in perm]
                if pair_sep:
                    text = pair_sep.join(pairs)
                else:
                    text = ''.join(pairs)
                total += 1
                if test_and_log(text, f"特定映射: {text}"):
                    return True
    
    # 也测试其他映射组合
    for field_perm in itertools.permutations(FIELD_NAMES):
        for value_perm in itertools.permutations(KNOWN_VALUES):
            pairs = list(zip(field_perm, value_perm))
            for kv_sep in ['=', ':']:
                for pair_sep in ['&', ',', '']:
                    pair_strs = [f"{k}{kv_sep}{v}" for k, v in pairs]
                    if pair_sep:
                        text = pair_sep.join(pair_strs)
                    else:
                        text = ''.join(pair_strs)
                    total += 1
                    if test_and_log(text, f"映射排列: {text}"):
                        return True
    
    # 8. 测试只有两个字段的映射
    print("[8] 两个字段的映射")
    for field_combo in itertools.combinations(FIELD_NAMES, 2):
        for value_combo in itertools.combinations(KNOWN_VALUES, 2):
            for field_perm in itertools.permutations(field_combo):
                for value_perm in itertools.permutations(value_combo):
                    pairs = list(zip(field_perm, value_perm))
                    for kv_sep in ['=', ':']:
                        for pair_sep in ['&', ',', ';', '']:
                            pair_strs = [f"{k}{kv_sep}{v}" for k, v in pairs]
                            if pair_sep:
                                text = pair_sep.join(pair_strs)
                            else:
                                text = ''.join(pair_strs)
                            total += 1
                            if test_and_log(text, f"两字段: {text}"):
                                return True
    
    # 9. 测试数组格式
    print("[9] 数组格式")
    for perm in itertools.permutations(KNOWN_VALUES):
        # [v1,v2,v3]
        text = '[' + ','.join(perm) + ']'
        total += 1
        if test_and_log(text, f"数组: {text}"):
            return True
        
        # [v1, v2, v3] (带空格)
        text = '[' + ', '.join(perm) + ']'
        total += 1
        if test_and_log(text, f"数组(空格): {text}"):
            return True
    
    # 10. 测试带引号的值
    print("[10] 带引号的值")
    for perm in itertools.permutations(KNOWN_VALUES):
        for sep in [',', ' ', '']:
            # "v1","v2","v3"
            text = sep.join([f'"{v}"' for v in perm])
            total += 1
            if test_and_log(text, f"引号: {text}"):
                return True
    
    print(f"\n总计测试: {total} 种组合")
    print("未找到匹配")
    
    with open('additional_patterns_results.txt', 'w') as f:
        f.write(f"额外模式测试结果\n")
        f.write(f"总测试数: {total}\n")
        f.write(f"结果: 未找到\n")
    
    return False

if __name__ == "__main__":
    found = main()
    if not found:
        print("\n详细结果已保存到 additional_patterns_results.txt")

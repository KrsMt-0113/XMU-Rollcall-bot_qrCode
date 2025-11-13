#!/usr/bin/env python3
"""
Brute Force Hash Analysis
暴力哈希分析 - 尝试找到产生目标哈希的输入

这个脚本会尝试各种可能的组合，包括:
- 添加额外的字符或字符串
- 使用不同的编码
- 测试是否有盐值(salt)
"""

import hashlib
import string

TARGET_HASH = "d89b99f96af9ff277008be738ca33795"
KNOWN_VALUES = ["78708", "1763018727", "230880"]

def md5(text):
    """计算MD5"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def test_with_salt():
    """测试加盐的情况"""
    print("=" * 80)
    print("测试加盐(Salt)的情况")
    print("=" * 80)
    
    # 常见的盐值
    common_salts = [
        '', 'salt', 'secret', 'key', 'token', 'xmu', 'rollcall', 'qrcode',
        '123', '456', '789', 'abc', 'xyz', 'admin', 'user', 'password',
        'tronclass', 'class', 'course', 'activity', 'data'
    ]
    
    found = False
    
    # 对每个已知值测试
    for val in KNOWN_VALUES:
        for salt in common_salts:
            # 盐在前
            text = salt + val
            h = md5(text)
            if h == TARGET_HASH:
                print(f"✓✓✓ 找到匹配! Salt在前: '{salt}' + '{val}'")
                print(f"完整输入: {text}")
                print(f"MD5: {h}")
                found = True
                
            # 盐在后
            text = val + salt
            h = md5(text)
            if h == TARGET_HASH:
                print(f"✓✓✓ 找到匹配! Salt在后: '{val}' + '{salt}'")
                print(f"完整输入: {text}")
                print(f"MD5: {h}")
                found = True
    
    # 测试组合值加盐
    for sep in ['', ',', '_', '-', ' ']:
        combined = sep.join(KNOWN_VALUES)
        for salt in common_salts:
            # 盐在前
            text = salt + combined
            h = md5(text)
            if h == TARGET_HASH:
                print(f"✓✓✓ 找到匹配! Salt在前: '{salt}' + 组合值")
                print(f"完整输入: {text}")
                print(f"MD5: {h}")
                found = True
                
            # 盐在后
            text = combined + salt
            h = md5(text)
            if h == TARGET_HASH:
                print(f"✓✓✓ 找到匹配! Salt在后: 组合值 + '{salt}'")
                print(f"完整输入: {text}")
                print(f"MD5: {h}")
                found = True
            
            # 盐在中间
            for i in range(1, len(KNOWN_VALUES)):
                parts = KNOWN_VALUES[:i] + [salt] + KNOWN_VALUES[i:]
                text = sep.join(parts)
                h = md5(text)
                if h == TARGET_HASH:
                    print(f"✓✓✓ 找到匹配! Salt在中间: '{salt}'")
                    print(f"完整输入: {text}")
                    print(f"MD5: {h}")
                    found = True
    
    if not found:
        print("未在常见盐值中找到匹配")
    
    return found

def test_with_prefix_suffix():
    """测试各种前缀和后缀"""
    print("\n" + "=" * 80)
    print("测试前缀和后缀组合")
    print("=" * 80)
    
    prefixes = ['', 'id:', 'code:', 'data:', 'value:', 'hash:', 'key:', 'token:']
    suffixes = ['', '&', ';', '|', '\n', '\r\n', '\t']
    
    found = False
    count = 0
    
    for val in KNOWN_VALUES:
        for prefix in prefixes:
            for suffix in suffixes:
                text = prefix + val + suffix
                h = md5(text)
                count += 1
                
                if h == TARGET_HASH:
                    print(f"✓✓✓ 找到匹配!")
                    print(f"前缀: '{prefix}'")
                    print(f"值: '{val}'")
                    print(f"后缀: '{repr(suffix)}'")
                    print(f"完整输入: {repr(text)}")
                    print(f"MD5: {h}")
                    found = True
    
    print(f"测试了 {count} 种组合")
    if not found:
        print("未找到匹配")
    
    return found

def test_number_formats():
    """测试不同的数字格式"""
    print("\n" + "=" * 80)
    print("测试不同的数字格式")
    print("=" * 80)
    
    found = False
    
    for val_str in KNOWN_VALUES:
        val_int = int(val_str)
        
        formats = [
            str(val_int),  # 标准整数
            f"{val_int:010d}",  # 10位零填充
            f"{val_int:015d}",  # 15位零填充
            f"{val_int:020d}",  # 20位零填充
            hex(val_int),  # 十六进制 (带0x)
            hex(val_int)[2:],  # 十六进制 (不带0x)
            oct(val_int),  # 八进制 (带0o)
            oct(val_int)[2:],  # 八进制 (不带0o)
            bin(val_int),  # 二进制 (带0b)
            bin(val_int)[2:],  # 二进制 (不带0b)
            f"{val_int:.2f}",  # 浮点数格式
            f"{val_int:.0f}",  # 浮点数格式(无小数)
        ]
        
        for fmt in formats:
            h = md5(fmt)
            if h == TARGET_HASH:
                print(f"✓✓✓ 找到匹配!")
                print(f"原始值: {val_str}")
                print(f"格式化后: {fmt}")
                print(f"MD5: {h}")
                found = True
    
    if not found:
        print("未在数字格式中找到匹配")
    
    return found

def test_double_hash():
    """测试双重或多重哈希"""
    print("\n" + "=" * 80)
    print("测试多重哈希")
    print("=" * 80)
    
    found = False
    
    for val in KNOWN_VALUES:
        # 双重MD5
        h1 = md5(val)
        h2 = md5(h1)
        
        if h1 == TARGET_HASH:
            print(f"✓✓✓ 找到匹配! (单次MD5)")
            print(f"输入: {val}")
            print(f"MD5: {h1}")
            found = True
        
        if h2 == TARGET_HASH:
            print(f"✓✓✓ 找到匹配! (双重MD5)")
            print(f"输入: {val}")
            print(f"第一次MD5: {h1}")
            print(f"第二次MD5: {h2}")
            found = True
        
        # 三重MD5
        h3 = md5(h2)
        if h3 == TARGET_HASH:
            print(f"✓✓✓ 找到匹配! (三重MD5)")
            print(f"输入: {val}")
            print(f"第三次MD5: {h3}")
            found = True
    
    # 测试组合值的多重哈希
    for sep in ['', ',', '_', ' ']:
        combined = sep.join(KNOWN_VALUES)
        h1 = md5(combined)
        h2 = md5(h1)
        
        if h1 == TARGET_HASH:
            print(f"✓✓✓ 找到匹配! (组合值单次MD5, 分隔符: '{sep}')")
            print(f"输入: {combined}")
            print(f"MD5: {h1}")
            found = True
        
        if h2 == TARGET_HASH:
            print(f"✓✓✓ 找到匹配! (组合值双重MD5, 分隔符: '{sep}')")
            print(f"输入: {combined}")
            print(f"双重MD5: {h2}")
            found = True
    
    if not found:
        print("未在多重哈希中找到匹配")
    
    return found

def test_with_timestamps():
    """测试是否包含时间戳"""
    print("\n" + "=" * 80)
    print("测试包含时间戳的情况")
    print("=" * 80)
    
    # 1763018727 看起来像一个Unix时间戳
    # 让我们检查一下
    import datetime
    
    ts = 1763018727
    try:
        dt = datetime.datetime.fromtimestamp(ts)
        print(f"1763018727 转换为日期时间: {dt}")
    except:
        print("1763018727 不是有效的Unix时间戳")
    
    # 测试其他可能的时间戳格式
    found = False
    
    # 可能是毫秒级时间戳
    ts_ms = ts * 1000
    h = md5(str(ts_ms))
    if h == TARGET_HASH:
        print(f"✓✓✓ 找到匹配! (毫秒级时间戳)")
        print(f"输入: {ts_ms}")
        print(f"MD5: {h}")
        found = True
    
    if not found:
        print("未在时间戳相关格式中找到匹配")
    
    return found

def main():
    """运行所有测试"""
    print("开始暴力哈希分析...")
    print(f"目标哈希: {TARGET_HASH}")
    print(f"已知值: {KNOWN_VALUES}")
    print()
    
    results = []
    
    # 运行各种测试
    results.append(('加盐测试', test_with_salt()))
    results.append(('前缀后缀测试', test_with_prefix_suffix()))
    results.append(('数字格式测试', test_number_formats()))
    results.append(('多重哈希测试', test_double_hash()))
    results.append(('时间戳测试', test_with_timestamps()))
    
    # 总结
    print("\n" + "=" * 80)
    print("暴力分析总结")
    print("=" * 80)
    
    found_any = False
    for test_name, found in results:
        status = "✓ 找到匹配" if found else "✗ 未找到"
        print(f"{test_name:20s}: {status}")
        if found:
            found_any = True
    
    if not found_any:
        print("\n所有测试均未找到匹配的哈希值")
        print("可能的原因:")
        print("1. 明文包含其他未知数据")
        print("2. 使用了复杂的盐值或密钥")
        print("3. 使用了自定义的哈希算法")
        print("4. 数据经过了其他形式的编码或加密")
    
    print("=" * 80)
    
    # 保存结果
    with open('brute_force_results.txt', 'w', encoding='utf-8') as f:
        f.write("暴力哈希分析结果\n")
        f.write("=" * 80 + "\n")
        f.write(f"目标哈希: {TARGET_HASH}\n")
        f.write(f"已知值: {KNOWN_VALUES}\n\n")
        
        for test_name, found in results:
            f.write(f"{test_name}: {'找到匹配' if found else '未找到'}\n")
        
        if not found_any:
            f.write("\n未能找到匹配的哈希值\n")
    
    print("\n结果已保存到 brute_force_results.txt")

if __name__ == "__main__":
    main()

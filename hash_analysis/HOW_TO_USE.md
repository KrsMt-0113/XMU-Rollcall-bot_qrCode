# 如何使用哈希分析工具 / How to Use Hash Analysis Tools

## 快速开始 / Quick Start

### 1. 运行所有自动化测试 / Run All Automated Tests

```bash
cd hash_analysis

# 运行基础分析
python3 hash_analysis.py

# 运行扩展分析
python3 extended_hash_analysis.py

# 运行暴力分析
python3 brute_force_analysis.py
```

### 2. 使用交互式工具 / Use Interactive Tool

#### 交互模式 / Interactive Mode
```bash
python3 interactive_hash_tool.py
```

然后输入你想测试的文本，工具会立即显示其MD5、SHA1和SHA256哈希值。

输入命令：
- `quit` 或 `exit` - 退出程序
- `test` - 运行快速测试
- 任何其他文本 - 计算该文本的哈希值

#### 命令行模式 / Command Line Mode
```bash
# 测试单个文本
python3 interactive_hash_tool.py "你的文本"

# 例如
python3 interactive_hash_tool.py "78708"
python3 interactive_hash_tool.py "78708,1763018727,230880"
```

## 文件说明 / File Description

| 文件 | 用途 | 测试数量 |
|------|------|---------|
| `hash_analysis.py` | 基础测试 | ~100 |
| `extended_hash_analysis.py` | 扩展测试 | 275+ |
| `brute_force_analysis.py` | 暴力测试 | 900+ |
| `interactive_hash_tool.py` | 交互式工具 | 按需 |

## 分析结果文件 / Result Files

运行脚本后会生成以下结果文件：

- `hash_analysis_results.txt` - 基础分析结果
- `extended_analysis_results.txt` - 扩展分析结果
- `brute_force_results.txt` - 暴力分析结果
- `MATCH_FOUND.txt` - 如果找到匹配，会创建此文件

## 自定义测试 / Custom Testing

如果你想测试自己的组合，可以：

1. **修改已知值**：编辑脚本顶部的 `KNOWN_VALUES` 列表
2. **添加新的测试用例**：在任何脚本中添加你自己的测试逻辑
3. **使用交互式工具**：最快捷的方式来测试各种组合

## 示例 / Examples

### 测试单个值
```bash
python3 interactive_hash_tool.py "78708"
```

### 测试组合
```bash
python3 interactive_hash_tool.py "78708,1763018727,230880"
```

### 测试特殊格式
```bash
python3 interactive_hash_tool.py '{"data":"78708"}'
```

## 目标哈希 / Target Hash

所有工具都在尝试找到产生以下哈希的输入：

**目标**: `d89b99f96af9ff277008be738ca33795`

如果任何工具找到匹配，它会：
- 在控制台显著地标记出来（✓✓✓）
- 创建 `MATCH_FOUND.txt` 文件保存结果
- 显示完整的输入文本

## 技术细节 / Technical Details

- 主要测试MD5哈希（32个十六进制字符）
- 也显示SHA1和SHA256用于比较
- 所有文本使用UTF-8编码
- 测试了900+种不同的组合和格式

## 支持 / Support

如果需要添加新的测试类型或有问题，请参考 `README.md` 获取更多信息。

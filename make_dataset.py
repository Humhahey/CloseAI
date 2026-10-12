
import json
import random
from pathlib import Path

# 40 个中文知识主题及答案
knowledge = [
    ("Python", "Python是一种编程语言，常用于自动化、数据分析、网站开发和人工智能。"),
    ("变量", "变量是用于保存数据的名称，程序可以通过变量读取和修改对应的值。"),
    ("列表", "列表是有序且可修改的数据容器，可以保存多个元素。"),
    ("字典", "字典使用键和值保存数据，适合通过键查找对应的值。"),
    ("函数", "函数把一段可复用的代码组织起来，可以接收参数并返回结果。"),
    ("循环", "循环可以让程序重复执行一段代码，常见的形式有for和while。"),
    ("类", "类是创建对象的蓝图，可以定义对象的属性和方法。"),
    ("异常处理", "异常处理可以捕获和处理程序运行时的问题，Python常用try和except。"),
    ("机器学习", "机器学习让计算机从数据中学习规律，并利用这些规律进行预测或分类。"),
    ("深度学习", "深度学习使用多层神经网络学习数据中的复杂模式。"),
    ("神经网络", "神经网络由相互连接的计算单元组成，通过训练调整参数来拟合数据。"),
    ("Transformer", "Transformer是一种神经网络架构，使用注意力机制学习序列中不同位置的关系。"),
    ("注意力机制", "注意力机制会根据当前任务给不同输入位置分配权重，再聚合相关信息。"),
    ("Token", "Token是模型处理文本时使用的基本单位，可以是字符、词或词的一部分。"),
    ("词表", "词表保存模型能够识别的Token及其编号，文本会先转换成编号再输入模型。"),
    ("Embedding", "Embedding把离散的Token编号映射为连续向量，使模型能够学习Token的表示。"),
    ("Logits", "Logits是模型输出的原始分数，通常还没有经过Softmax转换成概率。"),
    ("Softmax", "Softmax把一组分数转换成总和为一的概率分布。"),
    ("交叉熵损失", "交叉熵损失衡量模型预测与正确目标之间的差异，正确答案概率越低，损失通常越大。"),
    ("反向传播", "反向传播利用链式法则计算损失对模型参数的梯度。"),
    ("梯度", "梯度描述函数对参数的变化率，可以帮助优化器确定参数更新方向。"),
    ("优化器", "优化器根据梯度更新模型参数，Adam和随机梯度下降都是常见优化器。"),
    ("过拟合", "过拟合指模型过度适应训练数据，却不能很好地处理未见过的数据。"),
    ("训练集", "训练集是模型计算训练损失并通过反向传播更新参数时使用的数据。"),
    ("验证集", "验证集用于评估模型在未参与参数更新的数据上的表现，帮助判断泛化能力。"),
    ("测试集", "测试集通常用于模型开发完成后的最终评估，不应反复用来调参。"),
    ("Batch", "Batch是一批同时送入模型处理的样本，批量训练可以提高计算效率。"),
    ("Epoch", "Epoch通常指模型完整遍历一次训练数据。"),
    ("学习率", "学习率控制每次参数更新的步幅，过大可能不稳定，过小则可能收敛缓慢。"),
    ("Dropout", "Dropout在训练时随机屏蔽部分激活值，是一种常见的正则化方法。"),
    ("残差连接", "残差连接把输入绕过部分计算后加到输出上，有助于信息和梯度传播。"),
    ("LayerNorm", "LayerNorm对单个样本的特征进行归一化，有助于训练稳定。"),
    ("张量", "张量是表示标量、向量、矩阵及更高维数组的通用数据结构。"),
    ("PyTorch", "PyTorch是深度学习框架，提供张量运算、自动求导和神经网络模块。"),
    ("Git", "Git是分布式版本控制系统，可以记录代码变化并支持分支协作。"),
    ("HTTP", "HTTP是应用层通信协议，客户端和服务器可以使用它交换请求与响应。"),
    ("API", "API定义软件组件之间的交互方式，包括输入参数、操作和返回结果。"),
    ("数据库索引", "数据库索引可以加快部分查询，但也会占用存储空间并增加写入维护成本。"),
    ("SQL", "SQL是用于查询和操作关系型数据库的语言。"),
    ("缓存", "缓存暂存近期或经常使用的数据，以减少重复计算或较慢的访问操作。"),
]

# 10 种问法
patterns = [
    "什么是{topic}？",
    "{topic}是什么意思？",
    "请简单解释一下{topic}。",
    "能用通俗的话介绍{topic}吗？",
    "我刚开始学习，请告诉我{topic}是什么。",
    "学习技术时，{topic}有什么作用？",
    "请从初学者的角度解释{topic}。",
    "我不太理解{topic}，能给我讲讲吗？",
    "请用一段简短的话说明{topic}。",
    "关于{topic}，最基本的概念是什么？",
]

# 5 种问句变体。10 × 5 × 40 = 2000 条。
wrappers = [
    "{}",
    "你好，{}",
    "我想请教一个问题：{}",
    "麻烦你帮我解答一下：{}",
    "我正在学习相关知识。{}",
]

records = []
for topic_id, (topic, answer) in enumerate(knowledge):
    for pattern in patterns:
        question = pattern.format(topic=topic)
        for wrapper in wrappers:
            records.append({
                "topic_id": topic_id,
                "messages": [
                    {"role": "user", "content": wrapper.format(question)},
                    {"role": "assistant", "content": answer},
                ],
            })

assert len(records) == 2000, f"实际记录数量：{len(records)}"

# 打乱同一主题内的问法，但保留 topic_id，便于按主题划分训练集和验证集。
random.Random(20261012).shuffle(records)

path = Path("data.jsonl")
with path.open("w", encoding="utf-8") as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

# 检查文件是否能正确读取
with path.open("r", encoding="utf-8") as f:
    loaded = [json.loads(line) for line in f if line.strip()]

print(f"已生成：{path.resolve()}")
print(f"记录数量：{len(loaded)}")
print("第一条记录：")
print(json.dumps(loaded[0], ensure_ascii=False, indent=2))

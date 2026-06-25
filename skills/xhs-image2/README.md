# xhs-image2-skills

通过 GPT Image 2 API 生成图片，支持文生图、图生图，默认 3:4 竖版适配小红书。

## 适用 Agent

本 Skill 可用于支持 Skill 标准的 Agent 运行时，包括：

- **Claude Code** — 注册 skill 路径后通过自然语言调用
- **Codex** — 使用 `$skill-installer` 安装
- **OpenClaw** — 支持 OpenClaw Skill 格式
- 其他兼容 SKILL.md 的 Agent 框架

## 快速开始

```bash
# 1. 配置 API Key
echo "API_KEY=vg-你的key" > .env

# 2. 生成图片（每个 prompt 生成一张）
python scripts/generate.py --prompts "一只橘猫坐在窗台上，水彩画风"

# 3. 多张生成
python scripts/generate.py --prompts "咖啡店早晨氛围" "极简护肤品海报" "日系插画少女"
```

## 前置准备

1. 去 [tuanduobao.com](https://www.tuanduobao.com) 注册并创建 API Key（格式 `vg-xxx...`）
2. 价格约 **5 分/张**
3. 在 `.env` 中填入 `API_KEY=vg-你复制的key`

## 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--prompts` / `-p` | 提示词列表，每个提示词生成一张 | 必填 |
| `--size` | 图片比例 | `3:4` |
| `--resolution` | 分辨率（1k / 2k / 4k） | `1k` |

支持的图片比例：`1:1` `3:2` `2:3` `4:3` `3:4` `5:4` `4:5` `16:9` `9:16` `2:1` `1:2` `21:9` `9:21`

## 输出

图片保存到 `images/generated/{timestamp}_{seq}.png`，完成后展示所有图片路径。

## 生成示例

| 提示词 | 结果 |
|--------|------|
| 一只橘猫坐在窗台上看夕阳，水彩画风，温暖色调 | ![cat](images/generated/20260624_133541_1.png) |
| 极简风格护肤品海报，米白背景 | ![skincare](images/generated/20260624_133638_1.png) |
| 日系插画少女，樱花树下 | ![anime](images/generated/20260624_133820_2.png) |

## License

MIT

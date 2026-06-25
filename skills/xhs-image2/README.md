# xhs-image2-skills

通过 [团多宝 API](https://www.tuanduobao.com) 调用 **GPT Image 2** 生成图片，支持文生图、图生图，默认 3:4 竖版适配小红书。

## 快速开始

```bash
# 1. 配置 API Key
echo "API_KEY=vg-你的key" > .env

# 2. 生成图片（每个 prompt 生成一张）
python scripts/generate.py --prompts "一只橘猫坐在窗台上，水彩画风"

# 3. 多张
python scripts/generate.py --prompts "咖啡店早晨氛围" "极简护肤品海报" "日系插画少女"
```

## 前置准备

1. 注册 [团多宝](https://www.tuanduobao.com)
2. 导航栏 **Key** → **创建 API Key** → 复制保存（格式 `vg-xxx...`）
3. 首次使用需先充值（支持微信/支付宝）
4. 在 `.env` 中填入 `API_KEY=vg-你复制的key`

## 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--prompts` / `-p` | 提示词列表，每个提示词生成一张 | 必填 |
| `--size` | 图片比例 | `3:4` |
| `--resolution` | 分辨率（1k / 2k / 4k） | `1k` |

支持的图片比例：`1:1` `3:2` `2:3` `4:3` `3:4` `5:4` `4:5` `16:9` `9:16` `2:1` `1:2` `21:9` `9:21`

## 输出

图片保存到 `images/generated/{timestamp}_{seq}.png`，完成后展示所有图片路径。

## AI Agent Skill

本仓库包含 `SKILL.md`，可用于 Claude Code、Codex 等支持 Skill 的 Agent 运行时。注册 skill 路径后即可通过自然语言直接调用，例如：

> "帮我画一张橘猫水彩画"
> "生成3张护肤品海报图"

## License

MIT

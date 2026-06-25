from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

API_BASE_URL = "https://videoapi.ai-create.cn/api"
DEFAULT_SIZE = "3:4"
DEFAULT_RESOLUTION = "1k"
IMAGE_SAVE_DIR = BASE_DIR / "images" / "generated"

def _load_env():
    if not ENV_PATH.exists():
        return {}
    env = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip()
    return env

_ENV = _load_env()

def get_api_key():
    key = _ENV.get("API_KEY", "")
    if not key:
        print()
        print("您需要先配置 API Key 才能使用生图功能。打开 https://www.tuanduobao.com ，")
        print("注册登录后点击导航栏「Key」创建 API Key（格式: vg-xxx...），复制保存好。")
        print("首次使用记得先充值，支持微信/支付宝，GPT Image 2 约 5 分一张。")
        print(f"然后编辑 {ENV_PATH}，填入:")
        print()
        print("  API_KEY=vg-你复制的key")
        print()
        print("保存后重新运行即可。")
        exit(1)
    return key

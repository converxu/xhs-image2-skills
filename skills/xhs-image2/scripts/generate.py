import argparse, json, os, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.config import API_BASE_URL, DEFAULT_SIZE, DEFAULT_RESOLUTION, IMAGE_SAVE_DIR, get_api_key

API_KEY = get_api_key()
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
TASK_POLL_INTERVAL = 2
TASK_MAX_WAIT = 120


def submit_task(prompt: str, size: str = DEFAULT_SIZE, resolution: str = DEFAULT_RESOLUTION) -> str:
    url = f"{API_BASE_URL}/images/generate"
    body = json.dumps({
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": size,
        "resolution": resolution,
        "n": 1,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"提交任务失败: {e}")

    # 返回格式：{task_id: int, apimart_task_id: str, credits_cost: float}
    # 使用内部 task_id（int）查任务状态
    task_id = data.get("task_id")
    if task_id is not None:
        return str(task_id)

    # 备选：{code, data: [{task_id}]}
    if data.get("code") == 200:
        tasks = data.get("data", [])
        if tasks:
            tid = tasks[0].get("task_id")
            if tid:
                return str(tid)

    raise RuntimeError(f"API 返回格式异常: {data}")


def poll_task(task_id: str) -> dict:
    url = f"{API_BASE_URL}/tasks/{task_id}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    for _ in range(TASK_MAX_WAIT // TASK_POLL_INTERVAL):
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            time.sleep(TASK_POLL_INTERVAL)
            continue

        # 平铺格式 {id, status, result: {images: [...]}}
        if "status" in data:
            task_data = data
        # 嵌套格式 {code, data: {status, ...}}
        elif data.get("code") == 200:
            task_data = data.get("data", {})
            if isinstance(task_data, list):
                task_data = task_data[0] if task_data else {}
        else:
            time.sleep(TASK_POLL_INTERVAL)
            continue

        status = task_data.get("status", "")
        if status == "completed":
            return task_data
        elif status == "failed":
            err = task_data.get("result", {}).get("error", "未知错误")
            raise RuntimeError(f"任务失败: {err}")

        time.sleep(TASK_POLL_INTERVAL)

    raise RuntimeError(f"任务超时（{TASK_MAX_WAIT}秒）: task_id={task_id}")


def download_image(url: str, save_path: Path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(data)
    except Exception as e:
        raise RuntimeError(f"下载图片失败 {url}: {e}")


def generate(prompts: list[str], size: str, resolution: str):
    IMAGE_SAVE_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for i, prompt in enumerate(prompts):
        print(f"[{i+1}/{len(prompts)}] 提交: {prompt[:40]}...")
        try:
            task_id = submit_task(prompt, size, resolution)
            print(f"       task_id={task_id}, 等待生成...")
            task_data = poll_task(task_id)
            images = task_data.get("result", {}).get("images", [])
            if not images:
                raise RuntimeError("返回数据中无图片")
            raw_url = images[0].get("url", "")
            if isinstance(raw_url, list):
                raw_url = raw_url[0] if raw_url else ""
            if not raw_url:
                raise RuntimeError("图片 URL 为空")
            img_url = raw_url

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{ts}_{i+1}.png"
            save_path = IMAGE_SAVE_DIR / filename

            print(f"       下载图片...")
            download_image(img_url, save_path)
            results.append({"seq": i + 1, "prompt": prompt, "path": str(save_path)})
            print(f"       ✅ 已保存: {save_path}")
        except Exception as e:
            results.append({"seq": i + 1, "prompt": prompt, "error": str(e)})
            print(f"       ❌ 失败: {e}")

    print("\n========== 生成结果 ==========")
    for r in results:
        status = "✅" if "path" in r else "❌"
        path_or_err = r.get("path", r.get("error", ""))
        print(f"  {status} [{r['seq']}] {r['prompt'][:50]}...")
        print(f"     {path_or_err}")
    print("==============================")


def main():
    parser = argparse.ArgumentParser(description="xhs-image2 - 调用 GPT Image 2 API 生成图片")
    parser.add_argument("--prompts", "-p", nargs="+", required=True, help="提示词列表，每个提示词生成一张图")
    parser.add_argument("--size", default=DEFAULT_SIZE, help=f"图片比例，默认 {DEFAULT_SIZE}")
    parser.add_argument("--resolution", default=DEFAULT_RESOLUTION, help=f"分辨率，默认 {DEFAULT_RESOLUTION}")
    args = parser.parse_args()
    generate(args.prompts, args.size, args.resolution)


if __name__ == "__main__":
    main()

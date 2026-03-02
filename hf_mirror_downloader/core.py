import subprocess
import os
import sys
def _hf_executor(base_cmd: list, *args, **kwargs):
    """
    内部核心逻辑：处理参数解析与命令执行
    """
    env = os.environ.copy()
    env["HF_ENDPOINT"] = "https://hf-mirror.com"

    cmd = base_cmd.copy()

    for arg in args:
        # 对字符串参数也进行下划线替换，确保命令行输入 --local_dir 也能兼容
        normalized_arg = str(arg).replace('_', '-') if str(arg).startswith('-') else str(arg)
        cmd.append(normalized_arg)

    # 2. 处理关键字参数 (kwargs)
    for key, value in kwargs.items():
        arg_name = f"--{key.replace('_', '-')}"
        if value is True:
            cmd.append(arg_name)
        elif value is False or value is None:
            continue
        else:
            cmd.append(arg_name)
            cmd.append(str(value))

    print(f"🛠️  执行命令: {' '.join(cmd)}")
    
    try:
        # 移除 check=True，改用手动检查 returncode
        # 这样我们可以更优雅地处理错误，而不会直接喷出一堆 Python 堆栈
        result = subprocess.run(
            cmd, 
            env=env, 
            # text=True, # 如果需要捕获输出并处理，取消此行注释
            # capture_output=False # 默认为 False，确保 hf 的错误直接打印到屏幕
        )

        if result.returncode != 0:
            # 这里打印原生错误码
            print(f"\n❌ hf 进程返回错误 (Exit Code: {result.returncode})")
            # 退出程序，保持与原生 CLI 行为一致
            sys.exit(result.returncode)
        
        print("\n✨ 任务成功完成")

    except FileNotFoundError:
        print("❌ 错误: 未找到 'hf' 命令，请确保已安装 huggingface-cli。")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行过程中出现异常: {e}")
        sys.exit(1)
# --- 暴露给外部的函数 ---

def hfm(*args, **kwargs):
    """基础 hf 命令透传"""
    return _hf_executor(["hf"], *args, **kwargs)

def download(*args, **kwargs):
    """hf download 命令透传"""
    return _hf_executor(["hf", "download"], *args, **kwargs)

# --- 测试 ---
if __name__ == "__main__":
    # 调用 hfm 检查版本: hf --version
    # hfm(version=True) 
    
    # 下载模型: hf download Qwen3-Coder --local-dir ./dir
    # download_model("Qwen/Qwen3-Coder-Next", local_dir="./dir", resume_download=True)
    pass
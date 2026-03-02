import argparse
import sys
from hf_mirror_downloader.core import download, hfm

def hfm_console():
    # 抓取终端敲的所有内容，直接塞给 hfm
    hfm(*sys.argv[1:])

def download_console():
    """
    支持两种模式：
    1. 简写模式: hf-down <repo_id> <local_dir>
    2. 原生模式: hf-down <repo_id> --local-dir <local_dir> [其他参数]
    """
    args = sys.argv[1:]
    
    # 逻辑判断：
    # 如果只有两个参数，且这两个参数都不是以 '-' 开头
    # 那么我们判定为：第一个是 repo_id，第二个是 local_dir
    if len(args) == 2 and not args[0].startswith('-') and not args[1].startswith('-'):
        repo_id = args[0]
        local_dir = args[1]
        # 调用时将第二个参数明确转为关键字参数
        download(repo_id, local_dir=local_dir)
    else:
        # 否则，视为用户在写原生命令，直接透传
        download(*args)



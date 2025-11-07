from devman.file.copy import log


def confirm() -> bool:
    while True:
        flag = input("是否继续(y/n)...").strip().lower()  # 获取用户输入并处理为小写
        if flag.startswith("y"):  # 如果以'y'开头
            log.info("继续执行...")
            return True
        elif flag.startswith("n"):  # 如果以'n'开头
            log.info("退出程序...")
            return False
        log.info("无效输入，请输入'y'或'n'。")  # 提示用户输入无效，继续询问

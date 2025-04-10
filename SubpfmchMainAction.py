import os.path
import SubpfmchMainUI as mui
import ComStructs as cms

class CSubpfmchMainAction:
    def __init__(self, log_handler):
        self.log_handler = log_handler  # 传入日志处理器

    def switch_parsing(self, mainUI, log_file):
        """启动日志解析"""
        if not os.path.exists(log_file):
            print(f"ERR: file {log_file} doesn't exist!")
            return
        if not isinstance(mainUI, mui.CSubpfmchMainUI):
            return

        try:
            if self.log_handler.get_status() == cms.STS_LOGTHREAD_STOP:
                self.log_handler.start_reading(log_file)
                mainUI.log_button.config(text=cms.TEXT_LOGBTN_STOP)
            elif self.log_handler.get_status() == cms.STS_LOGTHREAD_RUN:
                self.log_handler.stop_reading()
                mainUI.log_button.config(text=cms.TEXT_LOGBTN_START)
        except Exception as e:
            print(f"启动日志解析时发生错误：{e}")

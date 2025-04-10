import tkinter as tk
import SubpfmchMainUI as mui
import SubpfmchMainAction as muia
import LogHandler as lgh
import DataDispatch as ddp


def update_entry():
    return

def main() -> None:
    """Program Entry"""
    # create data dispatch
    disp = ddp.CDataDispatch()
    # 创建日志处理器
    logHandler = lgh.CLogHandler(disp.dispatch)

    # create Main UI
    root = tk.Tk()
    mainUIAct = muia.CSubpfmchMainAction(logHandler)
    mainUI = mui.CSubpfmchMainUI(root, mainUIAct)
    mainUI.prepare()

    root.protocol("WM_DELETE_WINDOW", lambda: (logHandler.stop_reading(), root.destroy()))
    root.after(1000, update_entry)
    root.mainloop()  # 启动UI事件循环

if __name__ == "__main__":
    main()

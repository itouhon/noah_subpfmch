import tkinter as tk
import pfmchChartUI as pcui
import ComStructs as cms

class CSubpfmchMainUI:
    def __init__(self, root, act):
        self.root = root
        self.act = act
        self.root.title("SUB Usage Chart")
        # 初始情况下不加载组件布局
        self.paned = None
        self.top_frame = None
        self.bottom_frame = None
        self.chart_ui = None
        self.log_entry = None
        self.log_button = None
        self.chkcpubox = None
        self.chktskbox = None
        self.chkmembox = None
        self.cpusides_entry = None
        self.rowLog_frame = None
        self.rowCpu_frame = None
        self.chkcpu_sts = tk.BooleanVar()
        self.chktsk_sts = tk.BooleanVar()
        self.chkmem_sts = tk.BooleanVar()

        return

    def prepare(self):
        # 创建 PanedWindow 并禁用 sash 拖动
        self.paned = tk.PanedWindow(self.root,
                                    orient=tk.VERTICAL,
                                    sashrelief=tk.FLAT,  # 隐藏分割线样式
                                    sashwidth=0,  # 设置分割线宽度为0
                                    showhandle=False)  # 隐藏拖动把手
        self.paned.pack(fill=tk.BOTH, expand=True)

        # 顶部区域 (80%)
        self.top_frame = tk.Frame(self.paned, bg="black")
        self.paned.add(self.top_frame)

        # 底部区域 (20%)
        self.bottom_frame = tk.Frame(self.paned, bg="gray")
        self.paned.add(self.bottom_frame)

        # 设置固定比例
        self.update_pane_sizes()
        self.root.bind("<Configure>", lambda e: self.update_pane_sizes())

        # 初始化上部区域内容，
        # 初始化图表UI
        self.chart_ui = pcui.CpfmchChartUI(self.top_frame)

        # depart the bottom area
        self.rowLog_frame = tk.Frame(self.bottom_frame, bg="gray")
        self.rowLog_frame.pack(fill=tk.X, pady=2)
        self.rowCpu_frame = tk.Frame(self.bottom_frame, bg="gray")
        self.rowCpu_frame.pack(fill=tk.X, pady=2)

        # log file path Entry
        self.log_entry = tk.Entry(self.rowLog_frame, width=60)
        self.log_entry.pack(side=tk.LEFT, padx=2, pady=2)
        self.log_entry.insert(0, "log file path")
        self.log_entry.config(state="disabled")

        # log start button
        self.log_button = tk.Button(self.rowLog_frame, text=cms.TEXT_LOGBTN_START,
                                    command=lambda: self.act.switch_parsing(self, self.log_entry.get()))
        self.log_button.pack(side=tk.LEFT, padx=2, pady=2)

        # CPU check box
        self.chkcpubox = tk.Checkbutton(self.rowCpu_frame, text=cms.CHKBOX_CPU, variable=self.chkcpu_sts, bg="gray")
        self.chkcpubox.pack(side=tk.LEFT, padx=2, pady=2)

        # CPU sides entry
        self.cpusides_entry = tk.Entry(self.rowCpu_frame, width=20)
        self.cpusides_entry.pack(side=tk.LEFT, padx=2, pady=2)
        self.cpusides_entry.insert(0, "CPU sides")
        self.cpusides_entry.config(state="disabled")

        return

    def update_pane_sizes(self):
        """根据窗口大小更新窗格比例"""
        total_height = self.root.winfo_height()
        top_height = int(total_height * 0.8)
        bottom_height = total_height - top_height

        # 在Windows/Linux上禁用拖动的方法
        self.paned.paneconfig(self.top_frame, height=top_height)
        self.paned.paneconfig(self.bottom_frame, height=bottom_height)

        return



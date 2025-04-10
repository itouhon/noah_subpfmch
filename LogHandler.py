import re
import os
import time
import threading
import ComStructs as cms
import DBHandler as dbh

class CLogHandler:
    def __init__(self, callback):
        """initialize"""
        self.cpu_ptn = re.compile(cms.CPU_PATTERN)
        self.task_ptn = re.compile(cms.TASK_PATTERN)
        self.mem_ptn = re.compile(cms.MEM_PATTERN)
        self.stop_flag = True
        self.log_thread = None
        self.callback = callback
        return

    def start_reading(self, log_file: str) -> None:
        """启动日志读取线程"""
        if not os.path.exists(log_file):
            print(f"ERR: file {log_file} doesn't exist!")
            return

        self.stop_flag = False
        self.log_thread = threading.Thread(target=self.readlog_thread, args=(log_file,), daemon=True)
        if self.log_thread:
            self.log_thread.start()

        return

    def stop_reading(self) -> None:
        """停止日志读取线程"""
        if self.log_thread and self.log_thread.is_alive():
            self.stop_flag = True
            self.log_thread.join()

        return

    def readlog_thread(self, log_file: str) -> None:
        """parse log file"""
        if not os.path.exists(log_file):
            return

        with open(log_file, 'r', encoding='utf-8') as f:
            f.seek(0, 2)  # start to read from file tail
            while not self.stop_flag:
                line = f.readline()
                if line:
                    line = line.strip()
                    self.parseline(line)
                else:
                    time.sleep(1)

    def parseline(self, line: str) -> None:
        """parse the input string"""
        while True:
            # match cpu usage
            cpu_match = self.cpu_ptn.match(line)
            if cpu_match:
                pe, itime, usage = cpu_match.groups()
                # execute callback
                if self.callback:
                    self.callback({cms.UTABLE_NAME: cms.CPUUSAGE_TABLE,
                                   cms.FIELD_TIME: int(itime),
                                   cms.FIELD_COREID: int(pe),
                                   cms.FIELD_USAGE: int(usage)})
                break
            # match task usage
            task_match = self.task_ptn.match(line)
            if task_match:
                pe, itime, tid, usage = task_match.groups()
                if self.callback:
                    self.callback({cms.UTABLE_NAME: cms.TASKUSAGE_TABLE,
                                   cms.FIELD_TIME: int(itime),
                                   cms.FIELD_COREID: int(pe),
                                   cms.FIELD_TASKID: int(tid),
                                   cms.FIELD_USAGE: int(usage)})
                break
            # match memory usage
            mem_match = self.mem_ptn.match(line)
            if mem_match:
                pe, itime, mt, usage = task_match.groups()
                if self.callback:
                    self.callback({cms.UTABLE_NAME: cms.MEMUSAGE_TABLE,
                                   cms.FIELD_TIME: int(itime),
                                   cms.FIELD_COREID: int(pe),
                                   cms.FIELD_MEMTYPE: int(mt),
                                   cms.FIELD_USAGE: int(usage)})
                break
            break
        return

    def get_status(self) -> int:
        status = cms.STS_LOGTHREAD_STOP
        if self.log_thread and self.log_thread.is_alive():
            status = cms.STS_LOGTHREAD_RUN
        return status



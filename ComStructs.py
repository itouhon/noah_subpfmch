# database usage
DATABASE_NAME = "subpfmch.db"
UTABLE_NAME = "tableName"
CPUUSAGE_TABLE = "cpuTB"
TASKUSAGE_TABLE = "taskTB"
MEMUSAGE_TABLE = "memTB"
FIELD_ID = "id"
FIELD_TIME = "time"
FIELD_COREID = "coreid"
FIELD_TASKID = "taskid"
FIELD_MEMTYPE = "memtype"
FIELD_USAGE = "usage"
DB_TABLE_MAXRECORDS = 1000000

# regex pattern
CPU_PATTERN = r"\(PE(\d+)\)\s*Time\[(\d+)\]\s*CPU_Usage\[(\d+)%\]"
TASK_PATTERN = r"\(PE(\d+)\)\s*Time\[(\d+)\]\s*TaskID\[(\d+)\]\s*Task_Usage\[(\d+)%\]"
MEM_PATTERN = r"\(PE(\d+)\)\s*Time\[(\d+)\]\s*MemType\[(\d+)\]\s*Mem_Usage\[(\d+)%\]"

# log thread
STS_LOGTHREAD_STOP = 0
STS_LOGTHREAD_RUN = 1

# UI text
TEXT_LOGBTN_START = "Start"
TEXT_LOGBTN_STOP = "Stop"
CHKBOX_CPU = "CPU"
CHKBOX_TSK = "Task"
CHKBOX_MEM = "Mem"

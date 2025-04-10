import sqlite3
from typing import Dict
import ComStructs as cms

class CDBHandler:
    def __init__(self):
        """
        initialize database
        """
        self.connClosed = True
        self.open()
        self.cursor = self.conn.cursor()
        self.create_tables()

        return

    def create_tables(self) -> None:
        """
        create three tables : 1. cpu usage 2. task usage 3. mem usage
        """
        if self.connClosed:
            return

        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {cms.CPUUSAGE_TABLE} (
            {cms.FIELD_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {cms.FIELD_TIME} INTEGER,
            {cms.FIELD_COREID} INTEGER,
            {cms.FIELD_USAGE} INTEGER
        )""")
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {cms.TASKUSAGE_TABLE} (
            {cms.FIELD_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {cms.FIELD_TIME} INTEGER, 
            {cms.FIELD_COREID} INTEGER,
            {cms.FIELD_TASKID} INTEGER,
            {cms.FIELD_USAGE} INTEGER
        )""")
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {cms.MEMUSAGE_TABLE} (
            {cms.FIELD_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {cms.FIELD_TIME} INTEGER,
            {cms.FIELD_COREID} INTEGER,
            {cms.FIELD_MEMTYPE} INTEGER,
            {cms.FIELD_USAGE} INTEGER
        )""")
        self.conn.commit()

        return

    def clear_tables(self) -> None:
        """clear tables"""
        if self.connClosed:
            return

        self.conn.execute(f'DELETE FROM {cms.CPUUSAGE_TABLE}')
        self.conn.execute(f'UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="{cms.CPUUSAGE_TABLE}"')
        self.conn.execute(f'DELETE FROM {cms.TASKUSAGE_TABLE}')
        self.conn.execute(f'UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="{cms.TASKUSAGE_TABLE}"')
        self.conn.execute(f'DELETE FROM {cms.MEMUSAGE_TABLE}')
        self.conn.execute(f'UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="{cms.MEMUSAGE_TABLE}"')
        self.conn.commit()

        return

    def insert_data(self, table_name: str, data: Dict[str, any]) -> None:
        """
        Insert data into the specified table
        :param table_name: Name of the table
        :param data: Dictionary of field names and values to insert
        """
        if self.connClosed and not isinstance(data, dict):
            return

        fields = ""
        placeholders = ""
        values = []
        # 根据表名动态生成插入语句
        if table_name == cms.CPUUSAGE_TABLE:
            required_fields = {cms.FIELD_TIME, cms.FIELD_COREID, cms.FIELD_USAGE}
            if required_fields.issubset(data.keys()):
                fields = f"{cms.FIELD_TIME}, {cms.FIELD_COREID}, {cms.FIELD_USAGE}"
                placeholders = "?, ?, ?"
                values = [data[cms.FIELD_TIME], data[cms.FIELD_COREID], data[cms.FIELD_USAGE]]
            else:
                print(f"Data for {cms.CPUUSAGE_TABLE} must contain {required_fields}")
        elif table_name == cms.TASKUSAGE_TABLE:
            required_fields = {cms.FIELD_TIME, cms.FIELD_COREID, cms.FIELD_TASKID, cms.FIELD_USAGE}
            if required_fields.issubset(data.keys()):
                fields = f"{cms.FIELD_TIME}, {cms.FIELD_COREID}, {cms.FIELD_TASKID}, {cms.FIELD_USAGE}"
                placeholders = "?, ?, ?, ?"
                values = [data[cms.FIELD_TIME], data[cms.FIELD_COREID], data[cms.FIELD_TASKID], data[cms.FIELD_USAGE]]
            else:
                print(f"Data for {cms.TASKUSAGE_TABLE} must contain {required_fields}")
        elif table_name == cms.MEMUSAGE_TABLE:
            required_fields = {cms.FIELD_TIME, cms.FIELD_COREID, cms.FIELD_MEMTYPE, cms.FIELD_USAGE}
            if required_fields.issubset(data.keys()):
                fields = f"{cms.FIELD_TIME}, {cms.FIELD_COREID}, {cms.FIELD_MEMTYPE}, {cms.FIELD_USAGE}"
                placeholders = "?, ?, ?, ?"
                values = [data[cms.FIELD_TIME], data[cms.FIELD_COREID], data[cms.FIELD_MEMTYPE], data[cms.FIELD_USAGE]]
            else:
                print(f"Data for {cms.MEMUSAGE_TABLE} must contain {required_fields}")

        if fields != "" and placeholders != "":
            query = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})"
            try:
                self.cursor.execute(query, values)
                self.conn.commit()
            except Exception as e:
                print(f"Error inserting data: {e}")

        return

    def query_data(self, table_name: str, conditions=None):
        """
        query data
        :param table_name: table name
        :param conditions: query condition
        :return: query results
        """
        if self.connClosed:
            return None

        query = f"SELECT * FROM {table_name}"
        qRsults = None
        if isinstance(conditions, dict):
            where_clauses = []
            params = []
            for field, value in conditions.items():
                where_clauses.append(f"{field} = ?")
                params.append(value)
            if where_clauses:
                query += f" WHERE {' AND '.join(where_clauses)}"

            try:
                self.cursor.execute(query, params)
                qRsults = self.cursor.fetchall()
            except Exception as e:
                print(f"Error executing query: {e}")
        else:
            try:
                self.cursor.execute(query)
                qRsults = self.cursor.fetchall()
            except Exception as e:
                print(f"Error executing query: {e}")

        return qRsults

    def all_records(self, table_name: str) -> int:
        """
        Count the total number of records in the specified table
        :param table_name: Name of the table
        :return: Number of records in the table
        """
        if self.connClosed:
            return 0

        count = 0
        query = f"SELECT COUNT(*) FROM {table_name}"
        try:
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
        except Exception as e:
            print(f"查询表 {table_name} 的记录数时发生错误：{e}")

        return count

    def open(self):
        """
        open database connection
        """
        if self.connClosed:
            self.conn = sqlite3.connect(cms.DATABASE_NAME)
            self.connClosed = False

        return

    def close(self):
        """
        close database connection
        """
        if not self.connClosed:
            self.conn.close()
            self.connClosed = True

        return



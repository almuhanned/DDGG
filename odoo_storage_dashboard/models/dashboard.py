# -*- coding: utf-8 -*-
from odoo import tools
from odoo import fields, models


def get_size_directory(folder: str) -> int:
    from pathlib import Path
    return sum(p.stat().st_size for p in Path(folder).rglob('*'))


def display_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            break
        size /= 1024
    return f"{size:.1f} {unit}"


class OdooStorageDashboard(models.TransientModel):
    _name = 'odoo.storage.dashboard'
    _description = "Storage Dashboard"

    section1 = fields.Html(readonly=1, default=lambda self: self.get_section1())
    section2 = fields.Html(readonly=1, default=lambda self: self.get_section2())
    section3 = fields.Html(readonly=1, default=lambda self: self.get_section3())
    section4 = fields.Html(readonly=1, default=lambda self: self.get_section4())

    def get_values(self, parameter):
        cr = self._cr
        if parameter == "db_name":
            return cr.dbname
        if parameter == "postgres_version":
            cr.execute("SELECT version();")
            postgres_version = cr.fetchall()
            return postgres_version and postgres_version[0] and postgres_version[0][0]
        if parameter == "db_size":
            cr.execute("SELECT pg_size_pretty(pg_database_size('%s'));" % cr.dbname)
            db_size = cr.fetchall()
            return db_size and db_size[0] and db_size[0][0]
        if parameter == "filestore_size":
            filestore_path = tools.config.filestore(self._cr.dbname)
            return display_size(get_size_directory(filestore_path))

        if parameter == "large_tables":
            cr.execute("""
            SELECT
                relname as "Table",
                pg_size_pretty(pg_total_relation_size(relid)) As "Size",
                pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as "External Size",
                pg_total_relation_size(relid) As "Size No Pretty"
                
                
                FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;
   
            """)

            large_tables = cr.fetchall()
            return large_tables

    def get_section1(self):
        return """
        <p>
            <strong>Database Name:</strong> {db_name}<br/>
            <strong>Database Version:</strong> {postgres_version}<br/>
        </p>
        """.format(
            db_name=self.get_values('db_name'),
            postgres_version=self.get_values('postgres_version'),
        )

    def get_section2(self):
        return """
        <p style="text-align:center;font-weight:bold;">Database Size</p>
        <p style="text-align:center;font-weight:bold;font-size:40px;">{db_size}</p>
        """.format(
            db_size=self.get_values('db_size'),

        )

    def get_section4(self):
        return """
        <p style="text-align:center;font-weight:bold;">Filestore Size</p>
        <p style="text-align:center;font-weight:bold;font-size:40px;">{db_size}</p>
        """.format(
            db_size=self.get_values('filestore_size'),
        )

    def get_section3(self):
        rows = ""
        count = 0
        data = self.get_values('large_tables') or []

        def size_percent(value):
            total = sum([x[3] for x in data])

            if total == 0:
                return 0
            return round((value / total) * 100, 2)

        for each in data:
            count += 1

            table_name = each[0]
            size = each[1]
            external_size = each[2]
            size_no_pretty = size_percent(each[3])

            rows += """
            <tr>
            <td>{sl_no}</td>
            <td>{table_name}</td>
            <td>
                <table style="background:#e0e0e0;width:100%;min-width:150px">
                   <tr>
                        <td style="background:#00b8ff;color:Transparent;width:{size_no_pretty}%"> </td>
                        <td style="padding:2px;padding-right:8px;text-align:right;">{size_no_pretty}%</td>
                   </tr>
                </table>
               
            </td>
            <td>{size}</td>
            <td>{external_size}</td>
            </tr>
            """.format(sl_no=count, table_name=table_name, size=size, external_size=external_size, size_no_pretty=size_no_pretty)

        return """
        <table style="width:100%%" class="table table-striped">
            <tr>
                <th>#</th>
                <th>Database Table</th>
                <th></th>
                <th>Size</th>
                <th>External Size</th>
            </tr>
        %s
        </table>""" % rows




# Todo Storage Analysis of large tables. This month this table this value

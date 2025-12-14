import pymysql

# Patch version check for Django 6.0 compatibility
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

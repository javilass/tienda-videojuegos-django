# PyMySQL es el "driver" que permite a Python conversar con MySQL/MariaDB.
# Esta línea hace que Django lo use como si fuera "mysqlclient" (MySQLdb).
# Lo usamos porque se instala sin problemas en Windows.
import pymysql

pymysql.install_as_MySQLdb()

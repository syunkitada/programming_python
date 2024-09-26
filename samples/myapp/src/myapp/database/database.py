import logging

import pymysql.cursors

from myapp.config import config

LOG = logging.getLogger(__name__)


class DB:
    def __init__(self):
        database_conf = config.get_database()
        host = database_conf.get("host")
        port = database_conf.getint("port")
        user = database_conf.get("user")
        password = database_conf.get("password")
        database = database_conf.get("database")

        # Connect to the database
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def select(self):
        with self.conn:
            with self.conn.cursor() as cursor:
                sql = "CREATE DATABASE IF NOT EXISTS `myapp`;"
                cursor.execute(sql)

                sql = """
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8_bin NOT NULL,
  `password` varchar(255) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;
"""
                cursor.execute(sql)

                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ("webmaster@python.org", "very-secret"))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.conn.commit()

            with self.conn.cursor() as cursor:
                # Read a single record
                sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                cursor.execute(sql, ("webmaster@python.org",))
                result = cursor.fetchone()
                print(result)

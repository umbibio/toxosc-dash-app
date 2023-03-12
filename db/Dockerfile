FROM mariadb:10.7

ADD 00_fix_mysql_version.sh /root/00_fix_mysql_version.sh
ADD 01_fix_mysql_max_connections.sh /root/01_fix_mysql_max_connections.sh

RUN bash /root/00_fix_mysql_version.sh
RUN bash /root/01_fix_mysql_max_connections.sh

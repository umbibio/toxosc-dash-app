# default value for max_connections is too low and yields to errors when trying to spawn 
# several app server workers. We increase this setting from 150 to 2000. We need to assess
# whether this is enough or not. We may want to include SQL replicas instead of increasing
# further the max_connections setting for a single server.

cat <<EOT >> /etc/mysql/conf.d/my.cnf
[mysqld]
max_connections=2000

EOT

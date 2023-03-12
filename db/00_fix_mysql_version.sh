# MySQL python connector gets version from first part of the string in '5.5.5-10.6.4-MariaDB'
# MariaDB sets this to 5.5.5
# the connector complains because it expects MySQL version 5.7.4 or higher
# the fix is to configure MariaDB to report 5.7.99 to MySQL python connector
# MariaDB real version is 10.6.x. We parse the real version from current installation

ver=`mysql --version`
ver=`expr "$ver" : ".*\ \(.*\)-MariaDB"`
version="5.7.99-$ver-MariaDB"

echo "User is `whoami`"
echo "Setting version to: $version"

cat <<EOT >> /etc/mysql/conf.d/my.cnf
[server]
version=$version

EOT

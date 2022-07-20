#!/bin/bash
# create random password
PASSWDDB="123"

DBUSER="redes"
DBNAME="redesDB"

# If /root/.my.cnf exists then it won't ask for root password
if [ -f /root/.my.cnf ]; then

    mysql -e "CREATE DATABASE ${DBNAME} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
    mysql -e "CREATE USER ${DBUSER}@'localhost' IDENTIFIED BY '${PASSWDDB}';"
    mysql -e "GRANT ALL PRIVILEGES ON *.* TO '${DBUSER}'@'localhost';"
    mysql -e "FLUSH PRIVILEGES;"

# If /root/.my.cnf doesn't exist then it'll ask for root password   
else
    echo "Please enter root user MySQL password!"
    read -s rootpasswd
    mysql -u root -p${rootpasswd} -e "CREATE DATABASE ${DBNAME} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
    mysql -u root -p${rootpasswd} -e "CREATE USER ${DBUSER}@'localhost' IDENTIFIED BY '${PASSWDDB}';"
    mysql -u root -p${rootpasswd} -e "GRANT ALL PRIVILEGES ON *.* TO '${DBUSER}'@'localhost';"
    mysql -u root -p${rootpasswd} -e "FLUSH PRIVILEGES;"
fi

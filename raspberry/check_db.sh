PASSDB='123'

mysql -u redes -p${PASSDB} -e "use redesDB; select * from registro;"

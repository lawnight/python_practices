#让开服更开快速，不用sleep

port=`netstat -ano|grep 10001`

while [ -z "$port" ]
do
        port=`netstat -ano|grep 10001`
        sleep .6
done

pid=`ps aux | grep princess.server | grep -v grep | awk '{print $2}'`
echo $pid

cd /home/brgzadmin/online/server

tail -n 120 out.txt

if [ ! -n "$pid" ]; then
        echo -e "服务器启动报错，请联系程序检查。。。。";
        exit 1;
else
        echo "服务器正常启动,进程id:";
        echo $pid;
fi

sleep 1

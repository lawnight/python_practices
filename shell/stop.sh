#不用sleep，让开服，停服更加快捷

pid=`jps -l|grep com.digisky.female.princess.server.Start| awk '{print $1}'`

echo $pid

if [ -z "$pid" ]
then
        echo 'already stop'
        exit
fi

java -cp lib/*:resources:princess-server.jar com.digisky.female.princess.server.script.StopServer

count=1
while [ -e /proc/$pid ]
do
        let count++
        if [ $count -gt 111 ]
        then
                echo 'force kill server'
                kill -9 $pid
        fi
        sleep .5
done
echo 'stop server done!'

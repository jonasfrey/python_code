mcu=atmega328p
f_cpu=16000000
format=ihex
rate=19200
port=$1
programmer=stk500
target_file=$2

avrdude -F -p $mcu -P $port -c $programmer -b $rate -U flash:w:$target_file

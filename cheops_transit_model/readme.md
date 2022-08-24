# start 
```
sudo python3 main.py
```

# errors 
`can't open camera by index`

change the n_port_number 0-9 and try again
```python
o_camera = cv2.VideoCapture(n_port_number)
```


`ImportError: You must be root to use this library on linux.`

run with root/sudo 
```
sudo python3 main.py
```
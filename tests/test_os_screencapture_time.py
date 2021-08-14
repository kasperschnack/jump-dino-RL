import os
from timeit import default_timer as timer

start = timer()
for _ in range(100):
    os.system("screencapture -x -R0,0,100,100 filename.png")
end = timer()
print(end - start)

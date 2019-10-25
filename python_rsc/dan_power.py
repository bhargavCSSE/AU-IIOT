import redis
import time
r = redis.Redis(host='localhost', port = '6379', decode_responses=True, db=0)
while True:
     basedata = r.get("basedata")
     results = [float(i) for i in basedata.split(",")]
     power1, power2, p1pp2, vrms, _,_,_,_,_,_,_ = results
     print(power1)
     print(power2)
     time.sleep(1)

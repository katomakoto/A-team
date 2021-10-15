from multiprocessing import Array, Pool
import time
import os

class demo_mp():
    def __init__(self):
        self.val1 = list(range(5))
        self.val1.reverse()

    def _wait_timer(self, ts):
        time.sleep(ts/2)
        return ts

    def pool(self):
        print("-----------------------")
        st1 = time.time()
        with Pool(os.cpu_count()) as poolmanager:
            print('CPU count: ',os.cpu_count())
            results = poolmanager.map(self._wait_timer, self.val1)
        print(results)
        print("順番もok")
        print("Time with Pool: {}".format(time.time()-st1))
        print("-----------------------")
        st2 = time.time()
        ans = []
        for val in self.val1:
            ans.append(self._wait_timer(val))
        print(ans)
        print("Time for loop: {}".format(time.time()-st2))
        print("-----------------------")


if __name__ == "__main__":
    testcls = demo_mp()
    testcls.pool()

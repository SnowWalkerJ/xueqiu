import os


class Process(object):
    def __init__(self, log_file):
        self.log_file = log_file
        self.done = set()
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                self.done = set(f.read().split("\n"))

    def check(self, key):
        flag = key not in self.done
        self.done.add(key)
        return flag

    def finalize(self):
        with open(self.log_file, "w+") as f:
            f.write("\n".join(list(self.done)))

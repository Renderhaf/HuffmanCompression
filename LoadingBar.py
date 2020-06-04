import sys

class LoadingBar():
    def __init__(self, size = 1):
        self.size = size
        self.completed_symbol = "="
        self.work_symbol = "-"

    def update(self,precent):
        precent = round(precent, 2)
        filler = "=" * (int(precent) * self.size) + "-" * \
            ((100-int(precent)) * self.size)
        sys.stdout.write("|" + filler + "|" + str(precent) + "%\r")
        sys.stdout.flush()

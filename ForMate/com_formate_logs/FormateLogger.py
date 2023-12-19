import datetime
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from collections import defaultdict

class FormateLogger:



    @classmethod
    def enabled(cls):
        return True

    @classmethod
    def output_enabled(cls):
        return True

    @classmethod
    def log(cls, log_line):
        if FormateLogger.enabled:
            now = datetime.datetime.now()
            current_date = now.strftime("%Y_%m_%d")
            cls.logfile_path = "com_formate_logs/logs/formate_log-" + current_date + ".csv"
            with open(cls.logfile_path, "a+") as log_file:
                log_file.write(str(datetime.datetime.now()) + "," + log_line + "\n")
            if FormateLogger.output_enabled:
                print(str(datetime.datetime.now()) + "," + log_line + "\n")

    @classmethod
    def generate_chart(cls):
        style.use('default')

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)

        def animate():
            now = datetime.datetime.now()
            current_date = now.strftime("%Y_%m_%d")
            logfile_path = "logs/formate_log-" + current_date + ".csv"
            graph_data = open(logfile_path, 'r').read()
            lines = graph_data.split('\n')
            xs = []
            ys = []
            for line in lines:
                if len(line) > 1:
                    exact_time, what_thread, description, time_took = line.split(',')
                    xs.append(float(time_took))
                    # ys.append(float(y))
            ax1.clear()
            ax1.plot(xs, ys)

            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()
        animate()

    @classmethod
    def normalize_text(self, str):
        return re.sub(r'\W+', '', str)


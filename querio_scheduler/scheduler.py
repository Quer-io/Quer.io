import querio as q
import schedule
import time
import os


class Scheduler:

    def __init__(self, db_path: str,  table_name: str, save_path: str = "", time_string: str = "02:00"):
        self.i = q.Interface(db_path, table_name, save_path)
        self.save_path = save_path
        self.time_string = time_string

    def set_time(self, time_string: str):
        self.time_string = time_string

    def retrain(self):
        self.i.retrain_saved_models()
        self.i.save_models()
        self.i.clear_models()
        print("Successfully retrained saved models")

    def get_complete_path(self):
        return os.path.join(os.getcwd(), self.save_path)

    def run(self):
        schedule.every().day.at(self.time_string).do(self.retrain)
        print("Saved models path: " + self.get_complete_path()
              + "\nKeep this script running to retrain models every day at " + self.time_string
              + "\nYou can stop the script by pressing CTRL + C")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("Stopped")
            pass


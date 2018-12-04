import querio as q
import schedule
import time
import os
import logging


class Scheduler:

    def __init__(self, save_path: str = "", time_string: str = "02:00"):
        self.save_path = save_path
        self.time_string = time_string
        self.logger = logging.getLogger("QuerioScheduler")

    def set_time(self, time_string: str):
        self.time_string = time_string

    def set_path(self, save_path: str):
        self.save_path = save_path

    def retrain(self):
        ss = q.service.save_service.SaveService(self.save_path)
        files = ss.get_querio_files()
        for f in files:
            try:
                m = ss.load_file(f)
                db_path = m.db_path
                table_name = m.table_name
                i = q.Interface(db_path, table_name, self.save_path)
                i.load_models()
                i.retrain_models()
                i.save_models()
                self.logger.info("""Successfully retrained saved model '{}'"""
                                 .format(f))
            except q.interface.QuerioColumnError:
                self.logger.error("""Encountered an error when retraining model '{}'."""
                                  .format(f))
            continue
        print("Retraining completed")

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

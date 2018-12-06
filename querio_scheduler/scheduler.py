import querio as q
import schedule
import time
import os
import logging


class Scheduler:

    def __init__(self, save_path: str = os.path.join(os.getcwd(), ""), time_string: str = "02:00"):
        self.save_path = save_path
        self.time_string = time_string
        self.logger = logging.getLogger("QuerioScheduler")

    def set_time(self, time_string: str):
        self.time_string = time_string

    def set_path(self, save_path: str):
        self.save_path = os.path.join(os.path.normpath(save_path), "")

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

    def run(self):
        schedule.every().day.at(self.time_string).do(self.retrain)
        print("Saved models path: " + self.save_path
              + "\nKeep this script running to retrain models every day at " + self.time_string
              + "\nYou can stop the script by pressing CTRL + C")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nStopped")
            pass


if __name__ == '__main__':
    import sys
    s = Scheduler()
    if len(sys.argv) > 1:
        try:
            if '--help' in sys.argv:
                print("This script is made for retraining saved Querio models periodically.\n"
                      "By default the script uses its parent folder as path and 02:00 as the time to run.\n"
                      "\n"
                      "Arguments:\n"
                      "-t [time in HH:MM]   (example: -t 23:15)\n"
                      "-p [path]   (example: -p 'home/username/Querio Files')\n"
                      "--now   (to retrain all the models in the folder immediately and then exit)\n"
                      "--help   (for help)")
                exit()
            if '-t' in sys.argv:
                time_input = sys.argv[sys.argv.index('-t') + 1]
                s.set_time(time_input)
            if '-p' in sys.argv:
                path_input = sys.argv[sys.argv.index('-p') + 1]
                s.set_path(path_input)
            if '--now' in sys.argv:
                s.retrain()
                exit()
        except IndexError:
            print("Invalid arguments provided. Try running with the argument --help")
            exit()
    else:
        print("Run with argument --help for more information.\n")
    s.run()

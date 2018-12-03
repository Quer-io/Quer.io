##Querio Scheduler
A scheduler for retraining saved Querio models periodically.

###Usage
* The scheduler is run from a python shell in the directory where the Querio models are saved.  
* The scheduler must be initialized with the same database path and table name that were used for the creation of the models.
 ~~~~
 import querio_scheduler as qs
 db_path = "https:\\path.to.database:12345"
 table_name = "user"
 scheduler = qs.Scheduler(db_path, user)
 ~~~~
 Start the scheduler with
 ~~~~
 scheduler.run()
 ~~~~
 It will retrain the models every day at 02:00 as long as the python shell is open.  
 The scheduler can also be stopped by pressing CTRL + C.  
 Before running, the default time can be changed by inputting a time a time string (format HH:MM) with
~~~~
scheduler.set_time("03:15")
~~~~
 
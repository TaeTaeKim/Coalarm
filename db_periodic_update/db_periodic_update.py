
import db_update
import schedule
import time

periodic_update = db_update.DB_Update()

# Api_Data update
schedule.every().day.at("11:10").do(periodic_update.update_Api_Data)

# Vaccine_Data update
schedule.every().day.at("06:30").do(periodic_update.update_Corona_Vaccine_Data) 

# Corona_Data update
schedule.every().hour.at(":00").do(periodic_update.update_Corona_Data)

# Embassy_Data update
schedule.every().day.at("10:30").do(periodic_update.update_Embassy_Data) 

# Safety_Data update
schedule.every().monday.do(periodic_update.update_Safety_Data)

# Safety_Score update
schedule.every().hour.at(":01").do(periodic_update.update_Safety_Score)


while True:
    schedule.run_pending()
    time.sleep(1)

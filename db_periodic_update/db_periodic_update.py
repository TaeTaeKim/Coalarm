
import db_update
import schedule
import time

corona_update = db_update.AsyncTask()

# Api_Data update
schedule.every().day.at("11:00").do(corona_update.update_Api_Data)

# Vaccine_Data update
schedule.every().day.at("06:30").do(corona_update.update_Corona_Vaccine_Data) 

# Corona_Data update
schedule.every().hour.do(corona_update.update_Corona_Data)

# Embassy_Data update
schedule.every().day.at("10:30").do(corona_update.update_Embassy_Data) 

# Safety_Data update
schedule.every().monday.do(corona_update.update_Safety_Data)

# Safety_Score update
schedule.every(3).hours.do(corona_update.update_Safety_Score)


while True:
    schedule.run_pending()
    time.sleep(1)
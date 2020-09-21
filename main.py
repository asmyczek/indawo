from indawo.main import start_service
import time
import gc
import ntptime

time.sleep_ms(100)
gc.collect()

ntptime.settime()

start_service()
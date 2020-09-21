from indawo.main import start_service
import time
import gc

time.sleep_ms(100)
gc.collect()

start_service()
from datetime import datetime
from pytz import timezone
asia = timezone('Asia/Phnom_Penh')
print(asia)
p=datetime.now(asia).time()
print(p)
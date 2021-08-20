import pandas as pd

dt=pd.date_range(start='01/01/2010',end='01/01/2030',periods=None,freq='d',tz=None,normalize=False,name=None,closed=None)

calendar=pd.DataFrame(data=dt,index=None,columns=['Date calendar'],dtype='datetime64[ns]',copy=False)

calendar['Year']=dt.year
calendar['Year (2)']=dt.strftime('%y')
#calendar['Semester']=
calendar['Quarter']=dt.quarter
#calendar['Trimester']=
calendar['Month']=dt.month
calendar['Month name (3)']=dt.strftime('%b')
calendar['Month name']=dt.strftime('%B')
calendar['Day of year']=dt.dayofyear
calendar['Day number']=dt.day
calendar['Day name (3)']=dt.strftime('%a')
calendar['Day name']=dt.strftime('%A')
calendar['Week']=dt.week
calendar['Week day']=dt.weekday

calendar['Is month start']=dt.is_month_start
calendar['Is month end']=dt.is_month_end
calendar['Is quarter start']=dt.is_quarter_start
calendar['Is quarter end']=dt.is_quarter_end
calendar['Is year start']=dt.is_year_start
calendar['Is year end']=dt.is_year_end
calendar['Is leap year']=dt.is_leap_year

print(calendar)
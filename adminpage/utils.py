from adminpage.models import RoomServer,TemperatureStore
#get data as list
def weekList(room,week,month,year):
    data=list()
    avg=0
    temperature = TemperatureStore.objects.filter(room__buildingRoom=room).filter(date__year=year)
    count = 0
    print(room)
    if temperature.exists():
        for i in temperature:
            if month == i.date.month:
                if checkWeek(week,i.date.day):
                    count+=1
                    avg +=i.Temperature
                    data.append(i)
    if count!=0:
        avg = avg/count
    # print(data)
    return data,avg

# weekList("i5",4,9,2020)

#check week 1 -4
def checkWeek(week_day,weekly):
    if week_day == 1:
        if weekly >= 1 and weekly <= 7:return True
    elif week_day == 2:
        if weekly >= 8 and weekly <= 14: return True
    elif week_day == 3:
        if weekly >= 15 and weekly <= 21: return True
    elif week_day == 4:
        if weekly >= 22 and weekly <= 28: return True



#month data as list
def monthList(room,month,year):
    data = dict()
    anotherdata=dict()
    avgweek= dict()
    anotheravg = dict()
    count=0
    summation=0
    for i in range(1,5):
        data[i],avgweek[i]=weekList(room,i,month,year)
        if data[i] !=[]:
            count+=1
            anotherdata[i]=data[i]
            anotheravg[i] ="%.2f"%avgweek[i]
            summation +=avgweek[i]
    if count!=0:
        summation = summation/count
        summation="%.2f"%summation
    else:
        summation = None
    return anotherdata, anotheravg,summation

#check month
def checkMonth(month):
    if month==1:return "January"
    elif month == 2:return "February"
    elif month == 3:return "March"
    elif month == 4:return "April"
    elif month == 5:return "May"
    elif month == 6:return "June"
    elif month == 7:return "July"
    elif month == 8:return "August"
    elif month == 9:return "September"
    elif month == 10:return "October"
    elif month == 11:return "November"
    elif month == 12:return "December"
# annually report 
def annuallyList(room,year):
    data = dict()
    anothermonthly=dict()
    anotherdata=dict()
    avgmonthly=dict()
    avgweekly=dict()
    monthly= dict()
    count=0
    summation=0
    for i in range(1,13):
        data[i],avgmonthly[i],avgweekly[i]=monthList(room,i,year)
        if data[i]!={}:
            count+=1
            summation+= float(avgweekly[i])
            anotherdata[i] = data[i]
            anothermonthly[i]= avgweekly[i]
            monthly[i]=checkMonth(i)
    if count !=0:
        summation="%.2f"%(summation/count)
    else:
        summation = None
    # print(anotherdata)
    # print(anothermonthly)
    # print(monthly)
    print(summation)
    return  anotherdata,anothermonthly,monthly,summation

    
#!/usr/bin/env python
import script
import datetime
import sys

def main(args):
    flagTue = False
    flagFri = False
    flagSat = False
    arg3 = ""
    
    while(True):
        check = datetime.datetime.now()
        check_tuesday = ((int(check.weekday())==1 or int(check.weekday())==2) and int(check.hour) >= 6 and int(check.minute) >=1) and (not flagTue)
        check_friday = (int(check.weekday())==4 and int(check.hour)>=6 and int(check.minute)>=1 and (not flagFri))
        check_saturday = ((int(check.weekday())==5 or int(check.weekday())==6) and int(check.hour)>=6 and int(check.minute)>=1)  and (not flagSat)
        if(check_tuesday or check_friday or check_saturday):
            if (((int(check.weekday())==1 or int(check.weekday())==2) and int(check.hour) >= 6 and int(check.minute) >=1) or ((int(check.weekday())==5 or int(check.weekday())==6) and int(check.hour)>=6 and int(check.minute)>=1)):
                arg3 = "https://activemississauga.ca/#!registered-programs?search=2020%20badminton%20river%20grove"
                print "running sat or tue"
                print args
                for x in range(1,len(args),2):
                    script.call(args[x],args[x+1],arg3)
                if(int(check.weekday())==1):
                    flagTue = True
                    flagFri = False
                    flagSat = False
                else:
                    flagTue = False
                    flagFri = False
                    flagSat = True
            else:
                arg3 = "https://activemississauga.ca/#!registered-programs?search=2020%20badminton%20mississauga%20valley" 
                print "running friday"
                print args
                for x in range(1,len(args),2):
                    script.call2(args[x],args[x+1],arg3)
                flagTue = False
                flagFri = True
                flagSat = False
if __name__ == '__main__':
    sys.exit(main(sys.argv))

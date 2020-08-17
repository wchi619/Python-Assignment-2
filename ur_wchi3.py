#!/usr/bin/env python3
"""
OPS435 Assignment 2 - Fall 2019
Program: ur_wchi3.py
Author: William Chi

"""

import os
import sys
import argparse
import time

def get_login_rec():
    '''
    Grabs the latest results of "last -Fwi" and stores to variable. The function will iterate through the contents and splits the string into a filtered list containing any line with length of 15 (which is the total length of the log per line.
    '''
    last_recs = []  #Store records from last command into list

    last = str(os.system("last -Fwi >/dev/null 2>&1"))  #Supress output

    for i in last:
        temp_line = i.split()
        if len(temp_line) == 15:    #Only store the right info
            temp_rec = ' '.join(temp_line)
            last_recs.append(temp_rec)

    return last_recs

def other_login_recs(filelist):
    '''
    Attempts to open other files, filter and return as list.
    '''
    other_recs = []  #Store records from other files
    
    #Try to open file, if not possible raise exception
    try:
        f = open(filelist, 'r')
        last = f.readlines()

        for i in last:  #Grab only the right info we need (15 char len)
            temp_line = i.split()
            if len(temp_line) == 15:
                temp_rec = ' '.join(temp_line)
                other_recs.append(temp_rec)
        f.close() 
    except:
        print("Error: Please check file name.")
        exit()
    
    return other_recs

def host_user(file_list):
    '''
    This function will print the list of host IP's OR usernames depending on the --list call option.
    '''

    lhost = []  #Store list of host IP's
    luser = []  #Store list of user names

    if args.list == "host":
        string = "Host list in log file(s):"

        #Creates header
        for i in range(len(args.F)):
            string += (" " + args.F[i])
            print(string)
            print("=" * len(string))

        #Iterate through the list and get the third column (IP's)
        for i in file_list:
            temp_host = i.split()
            host = temp_host[2]
            lhost.append(host)
    
        #Remove duplicates and print all unique IP's
        dupe_host = set(lhost)
        for i in sorted(dupe_host):
            print(i)
    elif args.list == "user":
        string = "User list in log file(s):"

        #Creates header
        for i in range(len(args.F)):
            string += (" " + args.F[i])
        print(string)
        print("=" * len(string))
    
        #Iterate through list and get first column (hostnames)
        for i in file_list:
            temp_user = i.split()
            user = temp_user[0]
            luser.append(user)

        #Remove duplicates and print all unique users
        dupe_user = set(luser)
        for i in sorted(dupe_user):
            print(i)
    
def daily(nstart, nend):
    '''
    This function will list the days and total seconds a logged connection was active for.
    '''
    record = {}  #Key: days  Value: seconds
    total = 0    #Stores total seconds
    
    if args.user:       #Creates header
        daily_string = "Daily usage report for " + str(args.user)
        print(daily_string)
        print("=" * len(daily_string))
        print("Date          Usage in seconds")
    elif args.rhost:    #Creates header
        daily_string = "Daily usage report for " + str(args.rhost)
        print(daily_string)
        print("=" * len(daily_string))
        print("Date          Usage in seconds")

    #Converts string list into seconds (mktime), and subtract start and end date, then add value to dictonary based on key iteration from our for loop. 
    for nstart, nend in zip(nstart, nend):
        difference = time.mktime(time.strptime(nend)) - time.mktime(time.strptime(nstart))
        date = time.strftime("%Y %m %d", time.strptime(nend))
        record[date] = difference

    for date, second in record.items():  #Print date and seconds
        print(date + "    " + str(int(second)))
        total += second
    
    print("Total         " + str(int(total)))  #Print total seconds

def weekly(nstart, nend):
    '''
    This function will list the weeks and total seconds a logged connection was active for.
    '''

    record = {}  #Key: days  Value: seconds
    total = 0    #Stores total seconds

    #Creates header
    if args.user:
        daily_string = "Weekly usage report for " + str(args.user)
        print(daily_string)
        print("=" * len(daily_string))
        print("Week #          Usage in seconds")
    elif args.rhost:
        daily_string = "Weekly usage report for " + str(args.rhost)
        print(daily_string)
        print("=" * len(daily_string))
        print("Week #          Usage in seconds")
    
    #Converts string list into seconds (mktime), and subtract start and end date, then add value to dictonary based on key iteration from our for loop. 
    for nstart, nend in zip(nstart, nend):
        difference = time.mktime(time.strptime(nend)) - time.mktime(time.strptime(nstart)) 
        date = time.strftime("%Y %W", time.strptime(nend))
        record[date] = difference

    for week, second in record.items():  #Print week and seconds
        print(str(week) + "         " + str(int(second)))
        total += second
    
    print("Total           " + str(int(total)))  #Print total seconds

def monthly(nstart, nend):
    '''
    This function will list the months and total seconds a logged connection was active for.
    '''

    record = {}  #Key: days  Value: seconds
    total = 0    #Stores total seconds

    #Header creation
    if args.user:
        daily_string = "Monthly usage report for " + str(args.user)
        print(daily_string)
        print("=" * len(daily_string))
        print("Month #          Usage in seconds")
    elif args.rhost:
        daily_string = "Monthly usage report for " + str(args.rhost)
        print(daily_string)
        print("=" * len(daily_string))
        print("Month #          Usage in seconds")

    #Converts string list into seconds (mktime), and subtract start and end date, then add value to dictonary based on key iteration from our for loop. 
    for nstart, nend in zip(nstart, nend):
        difference = time.mktime(time.strptime(nend)) - time.mktime(time.strptime(nstart))
        date = time.strftime("%Y %m", time.strptime(nend))
        record[date] = difference

    for month, second in record.items(): #Print month and seconds
        print(str(month) + "          " + str(int(second)))
        total += second

    print("Total" + "            " + str(int(total))) #Print total seconds

def create_records(file_list):
    '''
    This function is the major component of the script. 
    This function will perform the following after preparing an array of all data records unique to the option input and filter the record to only contain dates for date manipulation in a list. The steps are as follows:

    /***BEGINNING OF START/END TIME LIST MANIPULATION PSEUDO CODE***/

    1. Convert start & end dates from string into datetime format.
    2. Convert the above into YYYY MM DD format (so we can sort and do date comparison later).
    3. If start/end dates are the same, automatically add entries into the final lists since we don't need to do anything with it anymore, we are looking for the ones that don't match.
    4. If the dates do not match, create a dummy entry for the start or end dates so we can subtract the dates later.
    5. Convert current iteration start time to seconds, then add 24 hours (1 day) and convert to local time.
    6. If the date of tomorrow, append the start/end dates to the list.
    7. If tomorrow doesnt equal the end date (of the iteration, loop through the list and keep appending dummy dates until there are no more dummy dates to add.
    '''

    dlist = []      #Nested array
    drecord = []    #Data record of unique entries
    tstart= []      #Appended start dates
    tend = []       #Appended end dates
    nstart = []     #Final modified start date
    nend = []       #final modified end date

    #Create nested list (array) of all log entries from file_list per each line
    for i in file_list:
        lines = i.split()
        dlist.append(lines)

    #Create data record of all entries unique to the user entry (of user or IP)
    if args.user:
        user = args.user
        for i in dlist:
            if user == i[0]:
                drecord.append(i)
    elif args.rhost:
        host = args.rhost
        for i in dlist:
            if host == i[2]:
                drecord.append(i)

    #Filter the data record (drecord) to only contain dates and store to temporary variables (tstart, tend)
    for i in drecord:
        start = i[3:8]
        end = i[9:14]
        tstart.append(" ".join(start))  #Join start elements together using spaces
        tend.append(" ".join(end))      #Join end elements together using spaces

    for start, end in zip(tstart, tend):
        tmp_start = time.strptime(start)
        tmp_end = time.strptime(end)
        
        convert_start = time.strftime("%Y %m %d", tmp_start)
        convert_end = time.strftime("%Y %m %d", tmp_end)

        if start[:10] == end[:10]:  #%a %m %d
            nstart.append(start)
            nend.append(end)
 
        if convert_end != convert_start:
            nstart.append(start)    #Append beginning start date
            nend.append(start[:10] + " 23:59:59 " + start[19:26])  #Add dummy END date
            sec_tomorrow = time.mktime(time.strptime(convert_start, "%Y %m %d"))
            string_tomorrow = time.ctime(sec_tomorrow + 86400) 
            tomorrow = time.strftime("%Y %m %d", time.strptime(string_tomorrow))
             
            if tomorrow == convert_end:
                nend.append(end)
                nstart.append(string_tomorrow)
            
            while tomorrow != convert_end:
                l_tomorrow = time.mktime(time.strptime(tomorrow, "%Y %m %d"))
                l_string = time.ctime(l_tomorrow)
                nstart.append(l_string)

                nend.append(l_string[:10] + " 23:59:59 " + l_string[20:26])
                tmp_tomorrow = time.mktime(time.strptime(tomorrow, "%Y %m %d"))
                tmp_string = time.ctime(tmp_tomorrow + 86400)
                tupule = time.strptime(tmp_string)
                tomorrow = time.strftime("%Y %m %d", tupule)

                if tomorrow == convert_end:
                    nend.append(tmp_string[:3] + end[3:])
                    nstart.append(tmp_string)

    #Correctly call function depending on --type option
    if args.type == "daily":
        daily(nstart, nend)
    elif args.type == "weekly":
        weekly(nstart, nend)
    elif args.type == "monthly":
        monthly(nstart, nend)
    
def verbose():
    '''
    This function will output additional information for verbosity when the option call -v is performed.
    '''

    print("Files to be processed:", args.F)
    print("Type of args for files:", type(args.F))
    
    if args.user:
        print("Usage report for user:", args.user)
    if args.rhost:
        print("Usage report for remote host:", args.rhost)
    if args.type:
        print("Usage report type:", args.type)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(epilog="Copyright 2019 - William Chi")
    parser.add_argument("F", nargs="+",  help="list of files to be processed")
    parser.add_argument("-l", "--list", choices=("user", "host"), help="generate username or remote host IP from the given file(s)")
    parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
    parser.add_argument("-t", "--type", choices=("daily","weekly","monthly"), help="type of report: daily, weekly, or monthly")
    parser.add_argument("-u", "--user",  help="usage report for the given username")
    parser.add_argument("-v", "--verbose", action="store_true", help="turn on output verbosity")
    args = parser.parse_args()
    
    #Stores file_list as a filtered log record of all files (including user entry files) to parse
    file_list = get_login_rec()
     
    #Grab and filter other logfiles
    for filelist in args.F:
        other_recs = other_login_recs(filelist)
        file_list += other_recs

   #Begin list options
    if args.list and args.verbose:
        verbose()
        host_user(file_list)
    else:
        host_user(file_list)
    
    #Begin report options (user or host)
    if args.user or args.rhost:
        if args.type and args.verbose:
            verbose()
            create_records(file_list)
        else:
            create_records(file_list)

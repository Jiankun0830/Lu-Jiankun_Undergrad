import time,datetime

StudentID = open('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\studentuserids.csv', 'r')
IDlist = StudentID.readlines()
StudentData_Final = {}

for i in range(len(IDlist)):
    IDlist[i] = IDlist[i][:-1]
    StudentData_Final[IDlist[i]] = {}

def AddToDataBase(filename, studentdata = StudentData_Final):
    myfile = open(filename, 'r')
    mylist = myfile.readlines()
    question_list = []

    for i in range(len(mylist)):
        linelist = mylist[i].split(';')
        linelist[3] = linelist[3][:-1]
        if linelist[3] not in question_list:
            question_list.append(linelist[3])

    for i in studentdata:
        for j in question_list:
            studentdata[i][j] = {}

    for i in range(len(mylist)):
        linelist = mylist[i].split(';')
        linelist[3] = linelist[3][:-1]
        studentdata[linelist[1]][linelist[3]][linelist[0]] = linelist[2]

    return studentdata

StudentData_Final = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek3.csv')
StudentData_Final = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek4.csv')
StudentData_Final = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek5.csv')
StudentData_Final = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek6.csv')
StudentData_Final = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek8.csv')


StudentData_Final_Ana = {}

for ID in StudentData_Final:
    StudentData_Final_Ana[ID] = {}
    for QuestionName in StudentData_Final[ID]:
        Actions = StudentData_Final[ID][QuestionName].values()
        StudentData_Final_Ana[ID][QuestionName] = []

        if 'submit-real' in Actions:
            Submission = True
        else:
            Submission = False
            StudentData_Final_Ana[ID][QuestionName] = [False, datetime.timedelta(0, 0, 0), 0]

        if Submission:
            CheckTimes = Actions.count('check')
            key_list = []
            for key in StudentData_Final[ID][QuestionName]:
                key_list.append(key)

            timeorder = key_list[:]
            timeorder.sort()
            timeorder.reverse()

            i = 0
            time_total = datetime.timedelta(0,0,0)

            while i < len(timeorder):
                if StudentData_Final[ID][QuestionName][timeorder[i]] == 'submit-real':
                    end_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.datetime(end_time[0],end_time[1],end_time[2],end_time[3],end_time[4],end_time[5])
                    i = i + 1
                    break
                i = i +1

            while i < len(timeorder):
                if StudentData_Final[ID][QuestionName][timeorder[i]] == 'access':
                    start_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                    start_time = datetime.datetime(start_time[0],start_time[1],start_time[2],start_time[3],start_time[4],start_time[5])
                    i = i + 1
                    break
                i = i + 1

            time_total = time_total + end_time - start_time

            while i < len(timeorder):
                while i < len(timeorder):
                    if StudentData_Final[ID][QuestionName][timeorder[i]] in ['submit-check', 'check']:
                        end_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                        end_time = datetime.datetime(end_time[0], end_time[1], end_time[2], end_time[3], end_time[4],end_time[5])
                        i = i + 1
                        break
                    i = i +1

                while i < len(timeorder):
                    if StudentData_Final[ID][QuestionName][timeorder[i]] == 'access':
                        start_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                        start_time = datetime.datetime(start_time[0], start_time[1], start_time[2], start_time[3],start_time[4], start_time[5])
                        i = i + 1
                        time_total = time_total + end_time - start_time
                        break
                    i = i + 1

            StudentData_Final_Ana[ID][QuestionName] = [True, time_total, CheckTimes]


StudentData_Output_Final = {}

StudentGrades = open('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\DW17Categories_SubsetWithID_forpython.csv')
StudentGrades_list = StudentGrades.readlines()

for i in StudentGrades_list:
    linelist = i.split(',')
    StudentData_Output_Final[linelist[0]] = [0, int(linelist[3])]

for ID in StudentData_Final_Ana:
    if ID in StudentData_Output_Final:
        num = 0
        for QuestionName in StudentData_Final_Ana[ID]:
            if StudentData_Final_Ana[ID][QuestionName][0]:
                num = num + 1
        StudentData_Output_Final[ID][0] = num


Output_Final = open('Output_Final.csv', 'w')

for ID in sorted(StudentData_Output_Final):
    writing = ID + ",%d,%d\n"%(StudentData_Output_Final[ID][0], StudentData_Output_Final[ID][1])
    Output_Final.write(writing)

Output_Final.close()




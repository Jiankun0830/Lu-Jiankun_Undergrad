import time,datetime

StudentID = open('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\studentuserids.csv', 'r')
IDlist = StudentID.readlines()
StudentData = {}
for i in range(len(IDlist)):
    IDlist[i] = IDlist[i][:-1]
    StudentData[IDlist[i]] = {}

def AddToDataBase(filename, studentdata = StudentData):
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

StudentData = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek3.csv')
StudentData = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek4.csv')
StudentData = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek5.csv')
StudentData = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek6.csv')
StudentData = AddToDataBase('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek8.csv')

StudentData_Ana = {}

for ID in StudentData:
    StudentData_Ana[ID] = {}
    for QuestionName in StudentData[ID]:
        Actions = StudentData[ID][QuestionName].values()
        StudentData_Ana[ID][QuestionName] = []

        if 'submit-real' in Actions:
            Submission = True
        else:
            Submission = False
            StudentData_Ana[ID][QuestionName] = [False,datetime.timedelta(0,0,0),0]

        if Submission:
            CheckTimes = Actions.count('check')
            key_list = []
            for key in StudentData[ID][QuestionName]:
                key_list.append(key)

            timeorder = key_list[:]
            timeorder.sort()
            timeorder.reverse()

            i = 0
            time_total = datetime.timedelta(0,0,0)

            while i < len(timeorder):
                if StudentData[ID][QuestionName][timeorder[i]] == 'submit-real':
                    end_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.datetime(end_time[0],end_time[1],end_time[2],end_time[3],end_time[4],end_time[5])
                    i = i + 1
                    break
                i = i +1

            while i < len(timeorder):
                if StudentData[ID][QuestionName][timeorder[i]] == 'access':
                    start_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                    start_time = datetime.datetime(start_time[0],start_time[1],start_time[2],start_time[3],start_time[4],start_time[5])
                    i = i + 1
                    break
                i = i + 1

            time_total = time_total + end_time - start_time

            while i < len(timeorder):
                while i < len(timeorder):
                    if StudentData[ID][QuestionName][timeorder[i]] in ['submit-check','check']:
                        end_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                        end_time = datetime.datetime(end_time[0], end_time[1], end_time[2], end_time[3], end_time[4],end_time[5])
                        i = i + 1
                        break
                    i = i +1

                while i < len(timeorder):
                    if StudentData[ID][QuestionName][timeorder[i]] == 'access':
                        start_time = time.strptime(timeorder[i], "%Y-%m-%d %H:%M:%S")
                        start_time = datetime.datetime(start_time[0], start_time[1], start_time[2], start_time[3],start_time[4], start_time[5])
                        i = i + 1
                        time_total = time_total + end_time - start_time
                        break
                    i = i + 1

            StudentData_Ana[ID][QuestionName] = [True,time_total,CheckTimes]



import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

X_Qustions = []
Y_Numbers = []
Y_Times = []
Y_TimeData = []

for i in sorted(StudentData_Ana[IDlist[0]]):
    X_Qustions.append(i)

for i in X_Qustions:
    Y_Numbers.append(0)
    Y_Times.append([])
    Y_TimeData.append(None)


for ID in StudentData_Ana:
    for i in StudentData_Ana[ID]:
        if StudentData_Ana[ID][i][0]:
            Y_Numbers[X_Qustions.index(i)] += 1
            if StudentData_Ana[ID][i][1].total_seconds() < 7200:
                Y_Times[X_Qustions.index(i)].append(StudentData_Ana[ID][i][1].total_seconds()/60)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % float(height))

X_range=range(len(X_Qustions))
rect = plt.bar(X_range, Y_Numbers, 0.4, color="green")
plt.xticks(X_range,X_Qustions)
plt.xlabel("Question Name")
plt.ylabel("Number of students")
plt.title("Number of students who do exercises")
autolabel(rect)
plt.show()
plt.close()

plt.boxplot(Y_Times,labels = X_Qustions)
plt.ylabel('Time(min)')
plt.xlabel('Question Name')
plt.show()
plt.close()



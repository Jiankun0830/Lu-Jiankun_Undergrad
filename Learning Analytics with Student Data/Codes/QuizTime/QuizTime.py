myfile = open('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ProgrammingQuizWeek4.csv', 'r')
mylist = myfile.readlines()
StudentData = {}
for i in range(len(mylist)):
    linelist = mylist[i].split(';')
    linelist[3] = linelist[3][:-1]

    if linelist[1] not in StudentData:
        StudentData[linelist[1]] = {}

    if linelist[3] not in StudentData[linelist[1]]:
        StudentData[linelist[1]][linelist[3]]={}

    StudentData[linelist[1]][linelist[3]][linelist[0]] = linelist [2]

import time,datetime

Output = []

for ID in StudentData:
    element = ID
    for QuestionName in StudentData[ID]:
        Submission = False
        Access_data_list = []
        Submit_data_list = []
        element = element +';' + QuestionName
        Actions = StudentData[ID][QuestionName].values()

        if 'submit-real' in Actions:
            Submission = True

        if Submission:
            for (key,value) in StudentData[ID][QuestionName].items():
                if value == 'submit-real':
                    SubmitTime = time.strptime(key, "%Y-%m-%d %H:%M:%S")
                    SubmitTime = datetime.datetime(SubmitTime[0],SubmitTime[1],SubmitTime[2],SubmitTime[3],SubmitTime[4],SubmitTime[5])
                    Submit_data_list.append(SubmitTime)
                elif value == 'access':
                    AccessTime = time.strptime(key, "%Y-%m-%d %H:%M:%S")
                    AccessTime = datetime.datetime(AccessTime[0], AccessTime[1], AccessTime[2], AccessTime[3],AccessTime[4], AccessTime[5])
                    Access_data_list.append(AccessTime)
            SubmitTime = max(Submit_data_list)
            AccessTime = min(Access_data_list)
            TimeSpent = SubmitTime - AccessTime
            element = element + ';' + str(TimeSpent)
        else:
            element = element + ';' + 'The student did not submit.'

    Output.append(element)

OutPutFile = open('ProgrammingQuizWeek4OutPut.txt','w')

for k in Output:
    OutPutFile.write(k + '\n')

OutPutFile.close()




myfile = open('C:\Users\lujia\Dropbox\UROP Summer 2017 (Yahan and Jiankun)\ExercisesWeek4.csv', 'r')
mylist = myfile.readlines()
StudentData = {}
for i in range(len(mylist)):
    linelist = mylist[i].split(';')
    linelist[3] = linelist[3][:-1]

    if linelist[1] not in StudentData:
        StudentData[linelist[1]] = {}
        StudentData[linelist[1]]['Wk.4.4.1'] = {}
        StudentData[linelist[1]]['Wk.4.4.2'] = {}
        StudentData[linelist[1]]['Wk.4.4.3'] = {}
        StudentData[linelist[1]]['Wk.4.4.4'] = {}
        StudentData[linelist[1]]['Wk.4.4.5'] = {}
        StudentData[linelist[1]]['Wk.4.4.6'] = {}


    StudentData[linelist[1]][linelist[3]][linelist[0]] = linelist [2]


Output = []

for ID in StudentData:
    element = 'ID:' + ID
    for QuestionName in StudentData[ID]:
        Submission = False
        element = element + ';' + QuestionName

        Actions = StudentData[ID][QuestionName].values()
        CheckTimes = Actions.count('check')
        if 'submit-real' in Actions:
            Submission = True

        element = element + ' ' + str(CheckTimes) + ' ' + str(Submission)

    Output.append(element)

OutPutFile = open('OutPut.txt','w')

for k in Output:
    OutPutFile.write(k + '\n')

OutPutFile.close()


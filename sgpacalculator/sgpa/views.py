from django.shortcuts import render
import getpass
import requests
from bs4 import BeautifulSoup

# Create your views here.
from django.http import HttpResponse
import os, sys

cwd=os.getcwd()
cwd+="/template"
sys.path.insert(0, cwd)


def home(request):
    return render(request, 'home.html')



def calculate_sgpa(request):
    UID = request.POST["uname"]
    PSW = request.POST["psw"]
    payload={"username":UID,"password":PSW}
    req=requests.post("https://academics.gndec.ac.in/",data=payload)
    cookies=req.cookies
    values={"final_exam_result_with_grades":"in"}
    rpost = requests.post("https://academics.gndec.ac.in", cookies=cookies, data=values)
    soup=BeautifulSoup(rpost.content,'html.parser')
    
    
    td_tags = list(soup.find_all('td'))
    #print(td_tags)
    candidate_name = td_tags[0].get_text()
    td_tags = td_tags[5:-32]  # Clearing the extra data
    
    subject_list = []
    temp_list = []
    count = 1
    for item in td_tags:
        if item.get_text()!='' and item.get_text()!=' ':
            temp_list.append(item.get_text())
        else:
    	    temp_list.append('0')
        if count == 13:
            count=1
            subject_list.append(temp_list)
            temp_list=[]
        else:
            count+=1
    
    #print(subject_list)
    
    fail_flag=0
    
    total_credit=0
    credit_grade_sum=0
    
    for subject in subject_list:
        if int(subject[-2]) >= 4:  # Grade >=4
            credit_grade_sum += int(subject[11])*int(subject[12])
            total_credit += int(subject[12])
        else:
            fail_flag=1
    
    
    #print(tabulate(subject_list,headers=["Semester","Subject Code","M code","Subject Title","Theory / Practical","Result Type","Internal Obtained Marks", "Internal Max. Marks", "External Obtained Marks", "External Max. Marks", "Grade Letter", "Grade Point", "Credits"]))
    
    sgpa=credit_grade_sum/total_credit
    
    if fail_flag!=1:
        string="""Congratulations Mr./Mrs. {} !!
    Your expected SGPA is {:0.2f}
    Your expected percentage is {:0.2f}%""".format(candidate_name, sgpa, sgpa*9.5)
    else:
        string="Sorry, your result cannot be displayed. Please check your result manually!"
    return render(request, 'result.html', {"result":string})

#def calculate_sgpa(request):
#    UID = request.POST["uname"]
#    PSW = request.POST["psw"]
#    string=str(UID)+str(PSW)
#    return render(request, 'result.html', {"result":string})

from django.shortcuts import render, redirect
from django.db.models import *
from django.views.generic import TemplateView
from mysite.forms import D31Form,MonthForm,CheckForm,D30Form,D28Form
from django.contrib.auth.decorators import login_required
from mysite.models import D31Info, UserStatus
import datetime

today = datetime.date.today()
this_month = today.month
#month_plus1 = this_month+1
month_plus1 = 4
def table_display(request,table_under_data1):
    table_display_dict=[]
    for data in table_under_data1:
        
        print(data.yasumi)
        print(data.month)
        print(data.user.username)

        
        if (data.month==2):#28日
            date=28
        elif (data.month==4) or (data.month==6) or (data.month==9) or (data.month==11):#30日
            date=30
        else:#31日
            date=31
        yasumi = data.yasumi.split(",")
        yasumi_list=[]
        z=1
        for i in yasumi:
            """
            print("休日は"+str(i))
            print("**********************")
            """
            for j in range(z,date+1):
                print("\niの値は"+str(i))
                print("zの値は"+str(z))
                print("jの値は"+str(j)+"\n")
                if j == int(i):
                    yasumi_list.append("〇")
                    print(str(j)+"日は〇")
                elif j < int(i):
                    yasumi_list.append(" ")
                    print(str(j)+"日は#")
                else:
                    z = j
                    print("zの値更新")
                    break
                zz=j
            
                #print(j)
        print("zzの値は"+str(zz))       
            #print("->"+str(z))
        for i in range(zz,date):
            yasumi_list.append(" ")
            print("空白追加")
        #default_dict = dict(month = month,Kiboukyuu = kiboukyuu )
        if date < 31:
            for i in range(date+1,31+1):
                yasumi_list.append("／")
        tmp_dict = dict(user=data.user.username,month = data.month,yasumi=yasumi_list)
        table_display_dict.append(tmp_dict)
        
    #print(table_display_dict)
    return table_display_dict
    






def kiboukyuu_hyouji(request):
    user = request.user
    if D31Info.objects.filter(user_id = user.id).exists():
        d31_data = D31Info.objects.filter(user_id = user.id)
        if d31_data.filter(status = 2).exists():
            d31_data = d31_data.filter(status = 2)
            d31_data = d31_data.order_by('month')
            exisitence = 1 #データがあるとき
        else:
            exisitence = 0 #データなし
    else:
        d31_data = ""
        exisitence = 0

    if D31Info.objects.filter(month = month_plus1).exists():
        table_data = D31Info.objects.filter(month = month_plus1)
        if table_data.filter(status = 2).exists():
            table_under_data2 = table_data.filter(status = 2)
            table_under_data2 = table_under_data2.order_by('table')
            table_display_dict = table_display(request,table_under_data2)
        else:
            table_under_data2 = []
            table_display_dict = {}
    else:
        table_under_data2 = []
        table_display_dict = {}

    return d31_data, exisitence, table_under_data2,month_plus1,table_display_dict
            
def form_display(request,month,monthform,d31_data,exisitence,table_under_data3,month_plus1,table_display_dict):
    a=1
    #print("form")
    user = request.user
    if D31Info.objects.filter(user_id = user.id).exists():
        data = D31Info.objects.filter(user_id = user.id)
        if data.filter(month = month).exists():
            data = data.filter(month = month)
            for i in data:  #pkを取得
                pk = i.id
            obj = D31Info.objects.get(id=pk)
            #print(obj.form)
            #print(obj.yasumi)
            kiboukyuu = obj.yasumi.split(',')
            default_dict = dict(month = month,Kiboukyuu = kiboukyuu )
            if (month==2):
                form = D28Form(request.GET or None, initial=default_dict)
            elif (month==4) or (month==6) or (month==9) or (month==11):
                form = D30Form(request.GET or None, initial=default_dict)
            else:
                form = D31Form(request.GET or None, initial=default_dict)
            
        else:
            request.session['monthform_data'] = request.POST
            default_dict = dict(month = month,Kiboukyuu = None)
            if (month==2):
                form = D28Form(request.GET or None, initial=default_dict)
            elif (month==4) or (month==6) or (month==9) or (month==11):
                form = D30Form(request.GET or None, initial=default_dict)
            else:
                form = D31Form(request.GET or None, initial=default_dict)
            
        a=2
        month_hyouji = str(month) + "月の希望休を選択"
        params ={
            'monthform':monthform,
            'form':form,
            'a':a,
            'month_hyouji':month_hyouji,
            'd31_data':d31_data, 
            'exisitence':exisitence,
            'table_under_data':table_under_data3,
            'month_plus1':month_plus1,
            'table_display_dict':table_display_dict
            
        }
        return params
    else:
        request.session['monthform_data'] = request.POST
        default_dict = dict(month = month,Kiboukyuu = None)
        if (month==2):
            form = D28Form(request.GET or None, initial=default_dict)
        elif (month==4) or (month==6) or (month==9) or (month==11):
            form = D30Form(request.GET or None, initial=default_dict)
        else:
            form = D31Form(request.GET or None, initial=default_dict)
        month_hyouji = str(month) + "月の希望休を選択"
        a=2
        params ={
                'monthform':monthform,
                'form':form,
                'a':a,
                'month_hyouji':month_hyouji,
                'd31_data':d31_data, 
                'exisitence':exisitence,
                'table_under_data':table_under_data3,
                'month_plus1':month_plus1,
                'table_display_dict':table_display_dict
            }
        return params

@login_required
def shihuto_submit(request):
    user = request.user

    d31_data, exisitence, table_under_data4,month_plus1,table_display_dict = kiboukyuu_hyouji(request)

    a = 1
    if request.method == 'POST':
        
        if 'month_button' in request.POST:
            monthform = MonthForm(request.POST)
            if monthform.is_valid():
                month = request.POST['month']
                #print(month)
                month = int(month)
                params = form_display(request,month,monthform,d31_data,exisitence,table_under_data4,month_plus1,table_display_dict)
                return render(request,'index.html',params)

        if 'yasumi_button' in request.POST:
            form = D31Form(request.POST)
            if form.is_valid():

                kiboukyuu = request.POST.getlist("Kiboukyuu")
                month = request.POST['month']
                yasumi =""
                for i in kiboukyuu:
                    yasumi += str(i)+","
                yasumi = yasumi[:-1]
                userstatus = UserStatus.objects.filter(user_id = user.id)
                pkk=0
                for i in userstatus:
                    pkk = i.id
                userstatus = UserStatus.objects.get(id=pkk)
                userstatus = userstatus.userstatus
                #print(yasumi +"/" +month)
                if D31Info.objects.filter(user_id = user.id).exists(): #最初のデータの有無
                    data = D31Info.objects.filter(user_id = user.id)
                    
                    if data.filter(month = month).exists(): #同じ月のデータが存在するか参照
                        #ある場合(上書き保存)
                        data = data.filter(month = month)
                        for i in data:
                            pk = i.id
                        obj = D31Info.objects.get(id=pk)
                        obj.yasumi = yasumi
                        obj.status = 1
                        obj.form = form
                        obj.table = userstatus
                        obj.save()
                        obj = obj
                    else:#同じ月のデータなし
                        D31Info(user = user, yasumi = yasumi,month = month,form = form,status = 1, table = userstatus).save()         
                        data = D31Info.objects.filter(user_id = user.id)       
                        data = data.filter(status =1)
                        #print(data.values())
                        for i in data:
                            pk = i.id
                        print(pk)
                        obj = D31Info.objects.get(id=pk)
                else: #一つもデータなし無い場合(そのまま保存)
                    D31Info(user = user, yasumi = yasumi,month = month,form = form,status = 1, table = userstatus).save()         
                    data = D31Info.objects.filter(user_id = user.id)       
                    data = data.filter(status =1)
                    #print(data.values())
                    for i in data:
                        pk = i.id
                    print(pk)
                    obj = D31Info.objects.get(id=pk)

                #print(data.id)
                params = {
                    'pk':pk,
                    'checkform':CheckForm(instance=obj),
                    'month':month,
                    'yasumi':yasumi,
                    'table_under_data':table_under_data4,
                    'month_plus1':month_plus1,
                    'table_display_dict':table_display_dict

                }
                return render(request,'check.html',params)

    else:
        monthform = MonthForm()

    return render(request, 'index.html',{'a':a,'monthform': MonthForm(),
                    'd31_data':d31_data, 
                    'exisitence':exisitence,'table_under_data':table_under_data4,'month_plus1':month_plus1
                    ,'table_display_dict':table_display_dict} )
    
def check(request,pk): #入力したフォーム内容を確認
    obj = D31Info.objects.get(id=pk)
    id = pk
    if(request.method == 'POST'):
        check_info = CheckForm(request.POST, instance = obj)
        #check_info.save()
        obj.status = 2
        obj.save()
        return redirect(to='/')


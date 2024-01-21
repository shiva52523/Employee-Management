from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.models import User, auth
from app.forms import EmployeeForm
from django.shortcuts import HttpResponse
from django.contrib import messages
from app.models import Employee
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView


def home(request):
    emp_data=Employee.objects.all()
    return render(request, 'app/home.html',{'emp_data':emp_data})


def register(request):
    emp_data=Employee.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save() 
                messages.success(request, 'Successfully Registered')
                return redirect(register)
                # return redirect('login_user')
        else:
            messages.warning(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        return render(request, 'app/registration.html',{'emp_data':emp_data})
 

def login_user(request):
    emp_data=Employee.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'app/login.html',{'emp_data':emp_data})


def logout_user(request):
    auth.logout(request)
    return redirect('logout_success')


def employee_data(request):
    emp_data=Employee.objects.all()
    form=EmployeeForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('success')
    return render(request,'app/empdataform.html',{'form':form,'emp_data':emp_data})


def get_emp_data(request):
    emp_data=Employee.objects.all()
    return render(request,'app/emp_data.html',{'emp_data':emp_data})


def success(request):
    emp_data=Employee.objects.all()
    return render(request, 'app/formsuccess.html',{'emp_data':emp_data})


def deleted(request):
    return render(request, 'app/deleted.html')



def update_view(request, id):
    context ={}
    emp = get_object_or_404(Employee, id = id)
    form = EmployeeForm(request.POST or None, instance = emp)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/app/detail/{}".format(id))
    context["form"] = form
    return render(request, "app/update_view.html", context)


def delete_view(request, id):
    context ={'id':id}
    emp = get_object_or_404(Employee, id = id)
    if request.method =="POST":
        emp.delete()
        return HttpResponseRedirect("/app/deleted")
    return render(request, "app/delete_view.html", context)


def sidebar(request):
    emp_data=Employee.objects.all()
    return render(request, 'app/sidebar.html',{'emp_data':emp_data})


class EmpDetail(DetailView):
    model = Employee
    def get_context_data(self,*args, **kwargs):
        context = super(EmpDetail, self).get_context_data(*args,**kwargs)
        context['emp_data'] = Employee.objects.all()
        return context
    

def logout_success(request):
    return render(request,'app/logout_success.html')




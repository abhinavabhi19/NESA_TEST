from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User,Task
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)


            if user.role == "SUPERADMIN":
                return redirect("superadmin_dashboard")

            elif user.role == "ADMIN":
                return redirect("admin_dashboard")

            else:
                return redirect("user_dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")



@login_required
def superadmin_dashboard(request):

    if request.user.role != "SUPERADMIN":
        return redirect("login")

    admins = User.objects.filter(role="ADMIN")
    users = User.objects.filter(role="USER")
    tasks = Task.objects.all()

    context = {
        "admins": admins,
        "users": users,
        "tasks": tasks
    }

    return render(request, "superadmin/dashboard.html", context)



@login_required
def create_admin(request):

    if request.user.role != "SUPERADMIN":
        return redirect("login")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            password=password,
            role="ADMIN"
        )

        return redirect("superadmin_dashboard")

    return render(request, "superadmin/create_admin.html")



@login_required
def create_user(request):

    if request.user.role != "SUPERADMIN":
        return redirect("login")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        admin_id = request.POST.get("admin")

        admin = User.objects.get(id=admin_id)

        User.objects.create_user(
            username=username,
            password=password,
            role="USER",
            assigned_admin=admin
        )

        return redirect("superadmin_dashboard")

    admins = User.objects.filter(role="ADMIN")

    return render(
        request,
        "superadmin/create_user.html",
        {"admins": admins}
    )


@login_required
def superadmin_tasks(request):

    if request.user.role != "SUPERADMIN":
        return redirect("login")

    tasks = Task.objects.select_related(
        "assigned_to",
        "assigned_by"
    ).all()

    return render(
        request,
        "superadmin/tasks.html",
        {"tasks": tasks}
    )




def logout_view(request):

    logout(request)

    return redirect("login")


# --------------------------------------------------------------
# admin 




@login_required
def admin_dashboard(request):

    if request.user.role != "ADMIN":
        return redirect("login")

    users = User.objects.filter(
        assigned_admin=request.user,
        role="USER"
    )

    tasks = Task.objects.filter(
        assigned_by=request.user
    )

    context = {
        "users": users,
        "tasks": tasks
    }

    return render(request, "admin/dashboard.html", context)


@login_required
def assign_task(request):

    if request.user.role != "ADMIN":
        return redirect("login")

    users = User.objects.filter(
        assigned_admin=request.user,
        role="USER"
    )

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        user_id = request.POST.get("user")

        assigned_user = User.objects.get(id=user_id)

        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_user,
            assigned_by=request.user,
            due_date=due_date
        )

        return redirect("admin_dashboard")

    return render(
        request,
        "admin/assign_task.html",
        {"users": users}
    )




@login_required
def admin_tasks(request):

    if request.user.role != "ADMIN":
        return redirect("login")

    tasks = Task.objects.filter(
        assigned_by=request.user
    )

    return render(
        request,
        "admin/tasks.html",
        {"tasks": tasks}
    )










# user --------------------------------------------------


@login_required
def user_dashboard(request):

    if request.user.role != "USER":
        return redirect("login")

    tasks = Task.objects.filter(assigned_to=request.user)

    pending_tasks = tasks.filter(status="PENDING")
    progress_tasks = tasks.filter(status="IN_PROGRESS")
    completed_tasks = tasks.filter(status="COMPLETED")

    context = {
        "tasks": tasks,
        "pending_count": pending_tasks.count(),
        "progress_count": progress_tasks.count(),
        "completed_count": completed_tasks.count(),
    }

    return render(request, "user/dashboard.html", context)




@login_required
def update_task(request, task_id):

    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if request.method == "POST":

        status = request.POST.get("status")
        report = request.POST.get("completion_report")
        hours = request.POST.get("worked_hours")

        task.status = status

        if status == "COMPLETED":
            task.completion_report = report
            task.worked_hours = hours

        task.save()

        return redirect("user_dashboard")

    return render(request, "user/update_task.html", {"task": task})




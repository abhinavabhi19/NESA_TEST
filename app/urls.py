from django.urls import path
from app import views


urlpatterns = [

    path("",
        views.login_view,
        name="login"),

    path(
        "superadmin/dashboard/",
        views.superadmin_dashboard,
        name="superadmin_dashboard"
    ),

    path(
        "superadmin/create-admin/",
        views.create_admin,
        name="create_admin"
    ),

    path(
        "superadmin/create-user/",
        views.create_user,
        name="create_user"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),



    # admin-----------------------------------------
    path("admin/dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
    ),

    path(
        "admin/assign-task/",
        views.assign_task,
        name="assign_task"
    ),

    path(
        "admin/tasks/",
        views.admin_tasks,
        name="admin_tasks"
    ),






    # user--------------------------------------------------
    path(
    "user/dashboard/",
    views.user_dashboard,
    name="user_dashboard"
    ),

    path(
        "user/task/<int:task_id>/update/",
        views.update_task,
        name="update_task"
    ),
]
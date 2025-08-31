from django.urls import path
from .views import index, user_register, taskList,user_login,task_create,task_update,task_delete,user_logout

urlpatterns = [
    path('', index, name='index'),
    path('register/',user_register,name='regiser'),
    path('tasks/',taskList,name='taskList'),
    path('login/',user_login,name='login'),
    path('task_create/',task_create,name='task_create'),
    path('task_update/<int:update_id>', task_update, name='task_update'),
    path('task_delete/<int:delete_id>', task_delete, name='task_delete'),
    path('logout',user_logout,name='user_logout'),

]
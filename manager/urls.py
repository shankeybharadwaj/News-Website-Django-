from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^panel/manager/list/$',views.manager_list , name='manager_list'),
    url(r'^panel/manager/del/(?P<pk>\d+)$',views.manager_del , name='manager_del'),
    url(r'^panel/manager/group/$',views.manager_group , name='manager_group'),
    url(r'^panel/manager/group/add/$',views.manager_group_add , name='manager_group_add'),
    url(r'^panel/manager/group/del/(?P<name>.*)$',views.manager_group_del , name='manager_group_del'), # deleting by name here (can also delete by pk)
    url(r'^panel/manager/group/show/(?P<pk>\d+)//$',views.user_groups , name='user_groups'),
    url(r'^panel/manager/addtogroup/(?P<pk>\d+)/$',views.add_user_to_group , name='add_user_to_group'),
    url(r'^panel/manager/del_group_from_user/(?P<pk>\d+)/(?P<name>.*)/$',views.del_group_from_user , name='del_group_from_user'),
    url(r'^panel/manager/perms/$',views.manager_perms , name='manager_perms'),
    url(r'^panel/manager/perms/del/(?P<name>.*)$',views.manager_perms_del , name='manager_perms_del'),
    url(r'^panel/manager/perms/add/$',views.manager_perms_add , name='manager_perms_add'),
    url(r'^panel/manager/perms/show/(?P<pk>\d+)/$',views.user_perms , name='user_perms'),
    url(r'^panel/manager/del_perm_from_user/(?P<pk>\d+)/(?P<name>.*)/$',views.del_perm_from_user , name='del_perm_from_user'),
    url(r'^panel/manager/add_perm_to_user/(?P<pk>\d+)/$',views.add_perm_to_user , name='add_perm_to_user'),
    url(r'^panel/manager/group_perms/(?P<name>.*)/$',views.group_perms , name='group_perms'),
    url(r'^panel/manager/del_perm_from_group/(?P<gname>.*)/(?P<pname>.*)/$',views.del_perm_from_group , name='del_perm_from_group'),
    url(r'^panel/manager/add_perm_to_group/(?P<name>.*)/$',views.add_perm_to_group , name='add_perm_to_group'),
]
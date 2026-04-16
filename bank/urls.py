from django.urls import path
from django.contrib.auth import views as auth_views
from bank import views
from bank.views import user_register_view, profile_edit, profile_view, create_branch_view, branch_detail_view, \
    update_branch, profile_page

urlpatterns = [
    path('register/', user_register_view, name='register'),
    path('profile/view/',profile_page, name='profile_view'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('add_bank/', views.add_bank, name='add_bank'),
    path('bank_list/', views.bank_list_view, name='bank_list'),
    path('banks/<int:bank_id>/details/', views.bank_detail_view, name='bank_details'),
    path('delete_bank/<int:bank_id>/', views.delete_bank, name='delete_bank'),
    path('banks/<int:bank_id>/branches/add/', create_branch_view, name='create_bank_branch'),
    path('banks/branch/<int:branch_id>/details/', branch_detail_view, name='branch_detail'),
    path('banks/branch/<int:branch_id>/edit/', update_branch, name='update_branch')

]

from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.create, name='create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('email/<int:email_id>/toggle_star/', views.toggle_star, name='toggle_star'),
    path('email/<int:email_id>/starred_toggle_star/', views.starred_toggle_star, name='starred_toggle_star'),
    path('starred/', views.starred_emails, name='starred_emails'),
    path('starred-to-bin/<int:email_id>/', views.starred_to_bin, name='starred_to_bin'),
    path('email/<int:email_id>/', views.email_detail, name='email_detail'),
    path('drafts/', views.drafts_emails, name='drafts_emails'),
    path('outbox/', views.outbox_emails, name='outbox_emails'),
    path('important/', views.important_emails, name='important_emails'),
    path('remove-important/<int:email_id>/', views.remove_important, name='remove_important'),
    path('important-to-bin/<int:email_id>/', views.important_to_bin, name='important_to_bin'),
    path('bin/', views.bin_emails, name='bin_emails'),
    path('bin/delete_all/', views.delete_all_bin_emails, name='delete_all_bin_emails'),
    path('bin/move/<int:email_id>/', views.move_to_bin, name='move_to_bin'),
    path('bin/recover/<int:email_id>/', views.recover_email, name='recover_email'),
    path('move_email/<int:email_id>/', views.move_email, name='move_email'),
    path('remove_draft/<int:email_id>/', views.remove_draft, name='remove_draft'),
    path('drafts-to-bin/<int:email_id>/', views.drafts_to_bin, name='drafts_to_bin'),
    path('delete/<int:email_id>/', views.delete_email, name='delete_email'),
    path('move-from-drafts/<int:email_id>/', views.move_from_drafts, name='move_from_drafts'),
]

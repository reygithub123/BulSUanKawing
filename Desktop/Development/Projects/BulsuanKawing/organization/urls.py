

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *

#self imports
from authorization.views import view_logout 

app_name ='org'

urlpatterns =[
    path('',view_org_dashboard, name="view-dashboard"),
    path('documents/',view_org_documents, name="view-documents"),
    path('documents/delete',view_delete_document, name="view-delete-document"),
    path('documents/submit',view_submit_document, name="view-submit-document"),
    path('documents/<int:doc_id>/',view_open_document, name="view-document"),
    path('documents/<int:doc_id>/change',view_change_file, name="view-change-file"),
    path('documents/<int:doc_id>/delete',view_delete_file, name="view-delete-file"),
    path('documents/<int:doc_id>/rename',view_rename_doc, name="view-rename-doc"),
    path('documents/<int:doc_id>/upload',view_upload_file, name="view-upload-file"),
    path('calendar/',CalendarView.as_view(), name="view-calendar"),
    path('events/',view_org_events, name="view-events"),
    path('events/add',view_add_event, name="view-add-event"),
    path('events/delete',view_delete_event, name="view-delete-event"),
    path('events/<int:ev_id>',view_edit_event, name="view-edit-event"),
    path('events/<int:ev_id>/adddoc',add_doc, name="add-event-doc"),
    path('gallery/',view_org_gallery, name="view-gallery"),
    path('gallery/add',add_album, name="add-album"),
    path('gallery/delete',delete_album, name="delete-album"),
    path('gallery/<int:album_id>',view_org_album, name="view-album"),
    path('gallery/<int:album_id>/rename',rename_album, name="rename-album"),
    path('gallery/<int:album_id>/upload',view_upload_images, name="upload-images"),
    path('gallery/<int:album_id>/delete',delete_images, name="delete-images"),
    path('me/',view_org_settings, name="view-me"),
    path('me/upload', profile_upload , name="profile-upload"),
    path('me/update', profile_update , name="profile-update"),
    path('me/account_update', account_update , name="account-update"),
    path('me/password', PasswordsChangeView.as_view(template_name='org-settings/change-password.html') , name="password-update"),
    path('me/password_success', redirect_success_change_pass , name="password-success"),
    path('workspace/',view_org_workspace, name="view-workspace"),
    path('workspace/delete',view_delete_work, name="view-delete-work"),
    path('workspace/rename',view_rename_wp, name="view-rename-wp"),
    path('workspace/<int:tdl_id>',view_org_edit_work, name="view-edit-work"),
    path('workspace/<int:tdl_id>/add',view_add_task, name="view-add-task"),
    path('workspace/<int:tdl_id>/<int:task_id>',view_org_edit_task, name="view-edit-task"),
    path('workspace/<int:tdl_id>/<int:task_id>/changestate',view_task_changestate, name="view-change-state"),
    path('workspace/<int:tdl_id>/<int:task_id>/delete',view_org_delete_task, name="view-delete-task"),
    path('setup/',view_account_setup, name="view-account-setup"),#x
    
    path('logout',view_logout, name="view-logout"),
]
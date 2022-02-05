
from django.urls import path
from .views import *

app_name ='cms'

urlpatterns =[
    path('',view_cms_dashbord , name="cms_land"),
    #cms
    path('changelogo/',change_logo , name="change-logo"),
    path('settings/',view_cms_account_setup , name="view-settings"),
    path('password/',PasswordsChangeView.as_view() , name="view-passwords"),
    path('password_success/',redirect_success_change_pass , name="password-success"),
    #documents
    path('documents/',view_pending_documents , name="view-pending-documents"),
    path('documents/<int:org_id>/',view_org_documents , name="view-org-documents"),
    path('documents/<int:org_id>/<int:doc_id>/',view_selected_document, name="view-document"),
    path('documents/<int:org_id>/<int:doc_id>/return/',return_document_email, name="return-document"),
    path('documents/<int:org_id>/<int:doc_id>/receive/',receive_document, name="receive-document"),
    #events
    path('calendar/',CMSCalendarView.as_view() , name="view-calendar"),
    path('events/',view_events, name="view-events"),
    path('events/add',view_add_event, name="view-add-event"),
    path('events/delete',view_delete_event, name="view-delete-event"),
    path('events/<int:ev_id>',view_edit_event, name="view-edit-event"),
    #organizations
    path('orgs/',view_organizations, name="view-organizations"), 
    path('orgs/<int:org_id>',view_organization, name="view-organization"), 
    path('orgs/<int:org_id>/events',view_organization_events, name="view-org-events"), 
    #gallery
    path('gallery/',view_gallery, name="view-gallery"),
    path('gallery/add',add_album, name="add-album"),
    path('gallery/delete',delete_album, name="delete-album"),
    path('gallery/<int:album_id>',view_album, name="view-album"),
    path('gallery/<int:album_id>/rename',rename_album, name="rename-album"),
    path('gallery/<int:album_id>/upload',view_upload_images, name="upload-images"),
    path('gallery/<int:album_id>/delete',delete_images, name="delete-images"),
    #news
    path('news/',view_news, name="view-news"),
    path('news/add',view_add_news, name="view-add-news"),
    path('news/delete',view_delete_news, name="view-delete-news"),
    path('news/<int:ev_id>',view_edit_news, name="view-edit-news"),
    
    #officers
    
    path('officers/',view_officers, name="view-officers"),
    path('officers/add',view_add_officer, name="view-add-officer"),
    path('officers/delete',view_delete_officer, name="view-delete-officer"),
    path('officers/<int:of_id>',view_edit_officer, name="view-edit-officer"),
]

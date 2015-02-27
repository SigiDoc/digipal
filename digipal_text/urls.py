from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('digipal_text.views',
    url(r'^digipal/manuscripts/(\d+)/texts/view/$', 'viewer.text_viewer_view'),
    #url(r'^admin/digipal/itempart/(\d+)/edit/([^/]+)/$', 'admin.text_view'),
    
    # Replace the first line with the second as apache doesn't like // (e.g. /texts/translation/whole//)
    # Django web server deals well with it. 
    #url(r'^digipal/manuscripts/(\d+)/texts/([^/]+)/([^/]+)/([^/]*)/$', 'viewer.text_api_view'),
    url(r'^digipal/manuscripts/(\d+)/texts/([^/]+)/([^/]+)/([^/]*)', 'viewer.text_api_view'),
)

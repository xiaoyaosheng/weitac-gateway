from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from services.views import ServiceViewSet
import services
from configurations.views import ConfigurationViewSet
# from events.views import
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'weitac-gateway.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', admin.site.urls),
                       url(r'^$', 'login.views.index'),
                       url(r'^index/$', 'login.views.index'),
                       url(r'^login/$', 'login.views.login'),
                       url(r'^logout/$', 'login.views.logout'),

                       url(r'^services_manage/$', 'services.views.get_services'),
                       url(r'^instance_manage/$', 'services.views.instance_manage'),

                       # url(r'^services_manage/$',
                       #     ServiceViewSet.as_view({'get': 'get_services',
                       #                             'post': 'delete_services',
                       #                             })),
                       url(r'^create_service/$', 'services.views.create_service'),

                       url(r'^update_service/$', 'services.views.update_service'),
                       url(r'^services/?',
                           ServiceViewSet.as_view({'post': 'create_service',
                                                   'put': 'update_services',
                                                   'delete': 'delete_services',
                                                   'get': 'get_services',
                                                   })),

                       url(r'^job_manage/$', 'jobs.views.job_manage'),
                       url(r'^job_upload/$', 'jobs.views.job_upload'),
                       url(r'^job_run/$', 'jobs.views.job_run'),
                       url(r'^job_periodictask/$', 'jobs.views.job_periodictask'),

                       url(r'^configuration_manage/$', 'configurations.views.configuration_manage'),
                       url(r'^configuration_upload/$', 'configurations.views.configuration_upload'),
                       url(r'^configuration_update/$', 'configurations.views.configuration_update'),
                       # url(r'^configuration/$', 'configurations.views.configuration_update'),
                       url(r'^configuration/?',
                           ConfigurationViewSet.as_view({'get': 'get_configuration',
                                                         'post': 'upload_configuration',
                                                         'put': 'update_configuration',
                                                         'delete': 'delete_configuration'})),
                       # url(r'^search_service/$','services.views.search_service'),
                       # url(r'^search_job/$','jobs.views.search_job'),

                       url(r'^event_handle/$', 'events.views.event_handle'),

                       # url(r'^create_service/$',
                       #     ServiceViewSet.as_view({'post': 'create_service'})),
                       # url(r'^create_service/$',
                       #     ServiceViewSet.as_view({'get': 'show_create_service',
                       #                             'post': 'create_service'})),

                       # url(r'^create_service/$',
                       #     ServiceViewSet.as_view({'post': 'create_service'})),
                       # url(r'^create_service/$',
                       #     ServiceViewSet.as_view({
                       #         'post': 'create_service',
                       #         'get': 'create_service',
                       #     })),

                       # url(r'^delete_services/$',
                       #     ServiceViewSet.as_view({'get': 'delete_services'})),
                       #
                       # url(r'^update_services/$', 'ServiceViewSet.update_services'),
                       #
                       # url(r'^search_ip/$', 'devmanage.views.search_ip'),
                       #
                       #

                       #
                       # url(r'^continer/?',
                       #     ServiceViewSet.as_view({'post': 'create_continer'
                       #                             # 'put': 'update_services',
                       #                             # 'get': 'get_services',
                       #                             # 'delete': 'delete_services'
                       #                             })),
                       )

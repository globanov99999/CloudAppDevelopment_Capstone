from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'djangoapp'
urlpatterns = [
                  path(route='about/', view=views.AboutPageView.as_view(), name='about'),
                  path(route='contact/', view=views.ContactPageView.as_view(), name='contact'),
                  path(route='signup/', view=views.signup_request, name='signup'),
                  path(route='login/', view=views.login_request, name='login'),
                  path(route='logout/', view=views.logout_request, name='logout'),
                  path(route='', view=views.get_dealerships, name='index'),
                  path(route='state/<int:state_id>/', view=views.get_dealers_by_state, name='dealers_by_state'),
                  path(route='dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
                  # path for add a review view
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

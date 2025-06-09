from django.contrib import admin
from reservation_app.models import Centre, Terrain, User

admin.site.register(User)
admin.site.register(Centre)
admin.site.register(Terrain)

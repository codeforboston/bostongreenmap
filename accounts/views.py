# Most of our views are currently provided by the django-profile App.

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Maybe? @login_required # or might that cause a loop in some obscure case?
def login_redirect(request):

    u = request.user

    if not (u.is_active and u.is_authenticated()):
        return redirect('home')

    p = u.get_profile()

    if p.favorite_park:
        return redirect(p.favorite_park)
    elif u.is_superuser or u.is_staff:
        return redirect('/admin/')

    return redirect('home')


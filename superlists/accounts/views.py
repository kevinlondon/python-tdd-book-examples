import sys
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

def login(request):
    print("login view", file=sys.stderr)
    # user = PersonaAuthenticationBackend().authenticate(request.POST['assetion'])
    user = authenticate(assertion=request.POST['assertion'])
    if user is not None:
        auth_login(redirect, user)
    return redirect("/")


def logout(request):
    auth_logout(request)
    return redirect("/")

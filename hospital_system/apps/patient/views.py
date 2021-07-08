from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def patient_signup_form(request):
    context = dict()
    if 'logged_email' in request.session:
        context['logged_email'] = request.session.get('logged_email')
        context['patient_type'] = True
    else:
        return HttpResponse('No LoggIn details provided')
    print(context)
    return render(request, 'signup.html', context=context)

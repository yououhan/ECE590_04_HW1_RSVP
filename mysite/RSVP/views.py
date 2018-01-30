from django.shortcuts import render

# Create your views here.
def sign_in(request):
    # View code here...
    return render(request, 'RSVP/test_sign_in.html')

def home(request):
    # View code here...
    return render(request, 'RSVP/test_main.html')

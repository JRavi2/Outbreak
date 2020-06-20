from django.shortcuts import render, redirect


def home(request):
    if request.POST:
        if 'disease' in request.POST:
            print("hello")
            return redirect('list_hospitals', disease=request.POST['disease'])
        if 'complaint' in request.POST:
            print('world')
            return redirect('initialize_chatbot', complaint=request.POST['complaint'])
    return render(request, 'home.html', {})
    # if request.user.is_authenticated:
    #     if request.user.user_type == 'P':
    #         return redirect('patient_dashboard')
    #     else :
    #         return redirect('hospital_dashboard')
    # else:
    #     return redirect('login')

from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from patients.forms import SignupForm, LoginForm, AppointmentForm


class Home(View):
    def get(self, request):
        return render(request, 'home.html')


class Register(View):
    def post(self, request):
        form_instance = SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('patients:login')
        else:
            print('error')
            return render(request, 'register.html', {'form': form_instance})

    def get(self, request):
        form_instance = SignupForm()
        context = {'form': form_instance}
        return render(request, 'register.html', context)


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from doctor.models import Doctor


class Login(View):
    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            u = form_instance.cleaned_data['username']
            p = form_instance.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user and user.is_superuser == True:
                login(request, user)
                return redirect('patients:home')
            elif user and user.is_superuser != True:
                login(request, user)
                return redirect('patients:home')
            else:
                messages.error(request, 'invalid credentials')
                return render(request, 'login.html', {'form': form_instance})

    def get(self, request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'login.html', context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('patients:login')


class Service(View):
    def get(self, request):
        return render(request, 'services.html')


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class Appointment(View):
    def post(self, request):
        form_instance = AppointmentForm(request.POST)
        if form_instance.is_valid():
            appointment = form_instance.save(commit=False)
            if request.user.is_authenticated:
                appointment.user = request.user

            # Razorpay Order Creation
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_amount = 25000
            order_currency = 'INR'
            payment_order = client.order.create(dict(amount=payment_amount, currency=order_currency, payment_capture=1))

            appointment.order_id = payment_order['id']
            appointment.save()

            context = {
                'appointment': appointment,
                'api_key': settings.RAZOR_KEY_ID,
                'order_id': payment_order['id'],
                'amount': payment_amount,
                'display_amount': 250
            }
            return render(request, 'payment.html', context)

        return render(request, 'appointment.html', {'form': form_instance})

    def get(self, request):
        doctor_id = request.GET.get('doctor_id')
        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                form_instance = AppointmentForm(initial={'doctor': doctor_id, 'department': doctor.department.id})
            except Doctor.DoesNotExist:
                form_instance = AppointmentForm()
        else:
            form_instance = AppointmentForm()
        context = {'form': form_instance}
        return render(request, 'appointment.html', context)


from patients.models import BookAppointment


class ShowAppointment(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('patients:login')
        user_appointments = BookAppointment.objects.filter(user=request.user, payment_status=True).order_by(
            '-appointment_date', '-time_slot')
        context = {'appointments': user_appointments}
        return render(request, 'account.html', context)


class CancelAppointment(View):
    def post(self, request, i):
        try:
            appointment = BookAppointment.objects.get(id=i, user=request.user)
            appointment.delete()
        except BookAppointment.DoesNotExist:
            pass
        return redirect('patients:show')


class PrintAppointment(View):
    def get(self, request, i):
        if not request.user.is_authenticated:
            return redirect('patients:login')
        try:
            appointment = BookAppointment.objects.get(id=i, user=request.user)
        except BookAppointment.DoesNotExist:
            return redirect('patients:show')
        context = {'appointment': appointment}
        return render(request, 'print_appointment.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccess(View):
    def post(self, request):
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        # Get the data from the request
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            appointment = BookAppointment.objects.get(order_id=razorpay_order_id)
            appointment.payment_status = True
            appointment.save()
            return redirect('patients:show')
        except:
            return redirect('patients:appointment')

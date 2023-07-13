
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseNotAllowed

from .models import Plan,PurchasePlan
import json
import paypalrestsdk
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta


def packages(request):
    user = request.user

    try:
        # Check if there is a current plan for the user
        current_plan = PurchasePlan.objects.select_related('plan').get(user=user)
        has_current_plan = True
    except PurchasePlan.DoesNotExist:
        has_current_plan = False
    except PurchasePlan.MultipleObjectsReturned:
        # If multiple current plans exist, retrieve the latest one
        current_plan = PurchasePlan.objects.select_related('plan').filter(user=user).latest('id')
        has_current_plan = True

    if has_current_plan:
        # There is a current plan, display only the current plan
        context = {'plan': current_plan.plan}
        return render(request, 'current_plan.html', context)
    else:
        # There is no current plan, display the available plans for purchase
        plans = Plan.objects.all()
        context = {'plans': plans}
        return render(request, 'packages.html', context)











def package_payment(request, plan_id):
    print('saaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas')
    if request.method == 'POST':
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        try:
            print('//////////////////')
            body = json.loads(request.body)
            print('ppppppppppppppppppppppppppppppppp',body)
            plan_id = body['planID']
            print('helloooooooooooooo',plan_id)
            plan = Plan.objects.get(id=plan_id)
            print('#####################')
            purchase_plan = PurchasePlan(user=request.user, plan=plan)
            print('haiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            purchase_plan.save()

            # Additional actions or saving payment-related information specific to the package payment

            return JsonResponse({'plan_id': plan_id, 'transID': body['transID']})
        except KeyError:
            return JsonResponse({'error': 'Invalid request body. Missing planID.'}, status=400)

    # Handle GET request for rendering the payment form
    package = get_object_or_404(Plan, pk=plan_id)
    your_paypal_client_id = settings.PAYPAL_CLIENT_ID
    context = {'package': package, 'your_paypal_client_id': your_paypal_client_id}
    return render(request, 'package_payment.html', context)

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_error(request):
    return render(request, 'payment_error.html')





def cancel_plan(request, plan_id):
    purchase_plan = get_object_or_404(PurchasePlan, id=plan_id, user=request.user)
    plan = purchase_plan.plan

    if plan.end_date and plan.end_date < timezone.now():
        plan.end_date = timezone.now()
        plan.save()

    purchase_plan.delete()
    return redirect('packages')

def current_plan(request):
    user = request.user

    try:
        # Retrieve the current plan for the user
        purchase_plan = PurchasePlan.objects.select_related('plan').filter(user=user).latest('id')
        plan = purchase_plan.plan

        if plan.end_date and plan.end_date < timezone.now():
            plan.end_date = timezone.now()
            plan.save()
            purchase_plan.delete()
            plan = None

        if not plan:
            raise PurchasePlan.DoesNotExist

        start_date = timezone.now()
        end_date = start_date + timedelta(days=plan.duration * 30)
        plan.start_date = start_date
        plan.end_date = end_date
        plan.save()

        context = {
            'plan': plan,
            'cancel_plan_id': purchase_plan.id
        }
    except PurchasePlan.DoesNotExist:
        plan = None
        context = {}

    if plan:
        # User already has a current plan, display the current plan instead of available plans
        return render(request, 'current_plan.html', context)
    else:
        # User doesn't have a current plan, check if there are any other active plans
        active_plans = PurchasePlan.objects.select_related('plan').filter(user=user, plan__end_date__gte=timezone.now())

        if active_plans:
            # There are active plans, retrieve the latest plan and display it
            latest_active_plan = active_plans.latest('id')
            plan = latest_active_plan.plan

            start_date = timezone.now()
            end_date = start_date + timedelta(days=plan.duration * 30)
            plan.start_date = start_date
            plan.end_date = end_date
            plan.save()

            context = {
                'plan': plan,
                'cancel_plan_id': latest_active_plan.id
            }
            return render(request, 'current_plan.html', context)
        else:
            # There are no current or active plans, display the available plans for purchase
            plans = Plan.objects.all()
            context['plans'] = plans
            return render(request, 'packages.html', context)

















from django.shortcuts import render
import json


# Create your views here.
def main(request):
    # violations = Violation.objects.all().values('latitude', 'longitude', 'address')
    #
    # context = {
    #     'violations': json.dumps(list(violations))
    # }

    return render(request, 'main.html')


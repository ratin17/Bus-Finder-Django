from django.urls import resolve
from .models import LogCount

class LogCounterMiddleware:
    
    TARGET_VIEWS = ['buses',
                    'bus',
                    'result',
                    'findBus',
                    'about',
                    'suggest_result',
                    'suggest_frac_result',
                    'suggest_custom',
                    'suggest_bus',
                    'suggest_bus_stand',
                    'suggest_stand',
                    'suggest_area',
                    'stands',
                    'stand',
                    'areas',
                    'area',
                    ]

    def __init__(self, get_response):
        # print("inside Init")
        self.get_response = get_response

    def __call__(self, request):
        # print("inside Call")
        response = self.get_response(request)
        
        current_view = resolve(request.path_info).view_name
        # print(current_view,self.TARGET_VIEWS)
        if current_view in self.TARGET_VIEWS:
            # print("inside if")
            request_count, created = LogCount.objects.get_or_create(id=1)
            request_count.count += 1
            # print(request_count.count)
            request_count.save()
        
        return response
    
    
    
    

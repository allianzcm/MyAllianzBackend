

from typing import Any


class CampusEmployeeMiddleWare():
   
   def __init__(self, get_response):
      self.get_response=get_response
      # One-time configuration and initialization.(continues on next page)3.3. Handling HTTP requests295
   
   def __call__(self, request) -> Any:
      # code to be executed for each request before the view
      # (and later middleware) are called.
      
      response = self.get_response(request)
      # code to be executed for each request/response after the view is called 
      
      return response
    
   def process_request(request):
      
      if request.user.is_authenticated():
            pass
         
   def process_view(request, view_func, view_args, view_kwargs):
      pass
      
   def process_exception(request, exception):
      pass
   def process_template_response(request, response):
      pass
   def process_response(request, response):
      pass


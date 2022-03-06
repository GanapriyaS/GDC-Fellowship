from datetime import datetime


class CustomMiddlleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialization
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view ( and later middleware ) are called
        """
        request.current_time = datetime.now()
        print("from a middleware request", request)

        # before response
        response = self.get_response(request)
        # after response
        return response

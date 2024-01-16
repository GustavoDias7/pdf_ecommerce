from datetime import datetime, timedelta


def payment_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        if "credit_card" in request.session:
            if "date" in request.session["credit_card"]:
                date = request.session["credit_card"]["date"]
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
                if datetime.now() >= date + timedelta(minutes=10):
                    del request.session["credit_card"]

        return response

    return middleware

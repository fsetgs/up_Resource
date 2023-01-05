from functools import wraps
from userControl.models import *
def check_identity(func):
    @wraps(func)
    def inner(request,*arg,**kwargs):
        login_company = request.session.get("company",None)
        company_obj = company.objects.get(name=login_company)
        if company_obj.code == "1":
            return func(request,*arg,**kwargs)
        else:
            pass
    return inner
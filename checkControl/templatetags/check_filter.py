from django import template
# 下面代码会直接使用register
register = template.Library()
from checkControl.models import *

@register.filter
def LongToShort(id):
    # 此id为盘点单id
    id=int(id)
    admin_objs = check_admin.objects.filter(t_check_id=id)
    content = []
    for admin_obj in admin_objs:
        content.append(admin_obj.name)
    if len(content) > 2:
        return ",".join(content) + "..."
    else:
        return ",".join(content)

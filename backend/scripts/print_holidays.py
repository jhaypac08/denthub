import os
import django
import json
from decimal import Decimal

import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'denthub_project.settings')
django.setup()

from website_content.models import Holiday
from website_content.serializers import HolidaySerializer

qs = Holiday.objects.all().order_by('is_recurring', 'month', 'day', 'specific_date', 'name')
serializer = HolidaySerializer(qs, many=True, context={})
print(json.dumps(serializer.data, default=str, indent=2))

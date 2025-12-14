from django.db import migrations, models
from decimal import Decimal


def create_holidays(apps, schema_editor):
    Holiday = apps.get_model('website_content', 'Holiday')
    # Truncate existing
    Holiday.objects.all().delete()

    entries = [
        # Regular Holidays (fixed)
        {"name": "New Year's Day", 'is_recurring': True, 'month': 1, 'day': 1, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': ''},
        {'name': 'Araw ng Kagitingan (Day of Valor)', 'is_recurring': True, 'month': 4, 'day': 9, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': ''},
        {'name': 'Labor Day', 'is_recurring': True, 'month': 5, 'day': 1, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': ''},
        {'name': 'Independence Day', 'is_recurring': True, 'month': 6, 'day': 12, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': ''},
        {'name': 'Bonifacio Day', 'is_recurring': True, 'month': 11, 'day': 30, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': ''},
        {'name': 'Christmas Day', 'is_recurring': True, 'month': 12, 'day': 25, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': ''},
        {'name': 'Rizal Day', 'is_recurring': True, 'month': 12, 'day': 30, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': ''},
        # Regular Holidays (movable / special observances)
        {'name': 'Maundy Thursday', 'is_recurring': True, 'month': None, 'day': None, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': 'Movable (Holy Week - date varies each year)'},
        {'name': 'Good Friday', 'is_recurring': True, 'month': None, 'day': None, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': 'Movable (Holy Week - date varies each year)'},
        {'name': 'National Heroes Day', 'is_recurring': True, 'month': 8, 'day': None, 'holiday_type': 'regular', 'pay_multiplier': Decimal('2.00'), 'notes': 'Observed on the last Monday of August'},
        # Special (non-working) holidays
        {'name': 'Chinese New Year', 'is_recurring': True, 'month': None, 'day': None, 'holiday_type': 'special_non_working', 'pay_multiplier': Decimal('1.30'), 'notes': 'Movable (date varies each year)'},
        {'name': 'EDSA People Power Anniversary', 'is_recurring': True, 'month': 2, 'day': 25, 'holiday_type': 'special_non_working', 'pay_multiplier': Decimal('1.30'), 'notes': ''},
        {'name': "Ninoy Aquino Day", 'is_recurring': True, 'month': 8, 'day': 21, 'holiday_type': 'special_non_working', 'pay_multiplier': Decimal('1.30'), 'notes': ''},
        {"name": "All Saints' Day", 'is_recurring': True, 'month': 11, 'day': 1, 'holiday_type': 'special_non_working', 'pay_multiplier': Decimal('1.30'), 'notes': ''},
        {'name': 'Black Saturday', 'is_recurring': True, 'month': None, 'day': None, 'holiday_type': 'special_non_working', 'pay_multiplier': Decimal('1.30'), 'notes': 'Movable (Holy Week - date varies each year)'},
        # Additional common special days
        {'name': 'Christmas Eve', 'is_recurring': True, 'month': 12, 'day': 24, 'holiday_type': 'special_non_working', 'pay_multiplier': Decimal('1.30'), 'notes': ''},
        {"name": "New Year's Eve", 'is_recurring': True, 'month': 12, 'day': 31, 'holiday_type': 'special_non_working', 'pay_multiplier': Decimal('1.30'), 'notes': ''},
    ]

    objs = []
    for e in entries:
        objs.append(Holiday(
            name=e.get('name'),
            is_recurring=e.get('is_recurring', True),
            month=e.get('month'),
            day=e.get('day'),
            specific_date=None,
            notes=e.get('notes',''),
            holiday_type=e.get('holiday_type','regular'),
            pay_multiplier=e.get('pay_multiplier', Decimal('1.00'))
        ))
    Holiday.objects.bulk_create(objs)


def reverse_func(apps, schema_editor):
    Holiday = apps.get_model('website_content', 'Holiday')
    Holiday.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website_content', '0007_holiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='holiday_type',
            field=models.CharField(max_length=32, default='regular', choices=[('regular', 'Regular Holiday'), ('special_non_working', 'Special (Non-Working)'), ('special_working', 'Special (Working)')], help_text='Type of holiday'),
        ),
        migrations.AddField(
            model_name='holiday',
            name='pay_multiplier',
            field=models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1.00'), help_text='Multiplier applied when employees work on this holiday (e.g., 1.30 for 30% additional, 2.00 for double pay)'),
        ),
        migrations.RunPython(create_holidays, reverse_func),
    ]

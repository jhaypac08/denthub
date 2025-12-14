from django.core.management.base import BaseCommand, CommandError
from website_content.models import Holiday
import datetime
from decimal import Decimal

try:
    from lunardate import LunarDate
except Exception:
    LunarDate = None


def easter_date(year: int) -> datetime.date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)


def last_monday_of_august(year: int) -> datetime.date:
    d = datetime.date(year, 8, 31)
    offset = (d.weekday() - 0) % 7
    return d - datetime.timedelta(days=offset)


class Command(BaseCommand):
    help = 'Expand recurring/movable holidays into concrete specific_date Holiday rows for a given year.'

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, help='Target year to expand', required=False)
        parser.add_argument('--commit', action='store_true', help='Persist generated specific_date holidays to DB')

    def handle(self, *args, **options):
        year = options.get('year') or datetime.date.today().year
        commit = options.get('commit')

        self.stdout.write(f'Expanding holidays for year {year} (commit={commit})')

        holidays = Holiday.objects.filter(is_recurring=True)
        created = 0
        to_create = []

        for h in holidays:
            computed = None
            name = (h.name or '').lower()

            # Specific date already present? skip
            if h.specific_date:
                continue

            # Fixed recurring with month/day
            if h.month and h.day:
                try:
                    computed = datetime.date(year, h.month, h.day)
                except Exception:
                    computed = None

            # Holy week-based
            if not computed and ('maundy' in name or 'good friday' in name or 'black saturday' in name or 'holy week' in (h.notes or '').lower()):
                try:
                    e = easter_date(year)
                    if 'maundy' in name:
                        computed = e - datetime.timedelta(days=3)
                    elif 'good friday' in name:
                        computed = e - datetime.timedelta(days=2)
                    elif 'black' in name:
                        computed = e - datetime.timedelta(days=1)
                except Exception:
                    computed = None

            # National Heroes Day: last Monday of August
            if not computed and 'national heroes' in name:
                try:
                    computed = last_monday_of_august(year)
                except Exception:
                    computed = None

            # Chinese New Year: use lunardate if available
            if not computed and 'chinese new' in name:
                if LunarDate is not None:
                    try:
                        # LunarDate(year,1,1) -> Gregorian date for lunar new year of that lunar year
                        computed = LunarDate(year, 1, 1).toSolarDate()
                    except Exception:
                        # try previous lunar year
                        try:
                            computed = LunarDate(year - 1, 1, 1).toSolarDate()
                        except Exception:
                            computed = None
                else:
                    self.stdout.write(self.style.WARNING('lunardate not installed; cannot compute Chinese New Year.'))

            if computed:
                # avoid duplicates
                exists = Holiday.objects.filter(is_recurring=False, specific_date=computed, name=h.name).exists()
                if exists:
                    self.stdout.write(f'Skipping existing {h.name} -> {computed}')
                    continue

                display = f'{h.name} -> {computed.isoformat()}'
                if commit:
                    new_h = Holiday(
                        name=h.name,
                        is_recurring=False,
                        month=None,
                        day=None,
                        specific_date=computed,
                        notes=(h.notes or '') + f' (expanded for {year})',
                        holiday_type=h.holiday_type,
                        pay_multiplier=h.pay_multiplier,
                    )
                    to_create.append(new_h)
                    created += 1
                    self.stdout.write(self.style.SUCCESS('Will create: ' + display))
                else:
                    self.stdout.write('Would create: ' + display)
            else:
                self.stdout.write(self.style.NOTICE(f'No computed date for {h.name}'))

        if commit and to_create:
            Holiday.objects.bulk_create(to_create)
            self.stdout.write(self.style.SUCCESS(f'Created {created} holiday rows for {year}'))
        else:
            self.stdout.write('Dry run complete.')

from rest_framework import serializers
from .models import HeroSection, Service, AboutSection, AboutFeature, ContactInfo, SiteSettings, Holiday
import datetime


def easter_date(year: int) -> datetime.date:
    """Return Easter Sunday date for given year (Anonymous Gregorian algorithm)."""
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

class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AboutFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutFeature
        fields = ['id', 'text', 'order']

class AboutSectionSerializer(serializers.ModelSerializer):
    features = AboutFeatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = AboutSection
        fields = '__all__'

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    computed_date = serializers.SerializerMethodField()

    class Meta:
        model = Holiday
        fields = ['id', 'name', 'is_recurring', 'month', 'day', 'specific_date', 'notes', 'holiday_type', 'pay_multiplier', 'created_at', 'computed_date']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """Allow recurring holidays without strict month/day for movable holidays (notes should explain rule).
        Require specific_date only for non-recurring entries."""
        is_rec = data.get('is_recurring', True)
        specific = data.get('specific_date')
        if not is_rec and not specific:
            raise serializers.ValidationError('Non-recurring holidays require specific_date')
        return data

    def get_computed_date(self, obj):
        """Return a concrete date for the holiday for a given year.

        Looks for a `year` query param on the request; falls back to current year.
        Computes:
        - specific_date if set
        - fixed recurring holidays (month/day)
        - Maundy Thursday / Good Friday / Black Saturday via Easter calculation
        - National Heroes Day (last Monday of August)
        For movable holidays we can't compute (e.g., Chinese New Year), returns None and preserves `notes`.
        """
        request = self.context.get('request') if isinstance(self.context, dict) else None
        year = None
        if request is not None:
            try:
                year_param = request.query_params.get('year')
                if year_param:
                    year = int(year_param)
            except Exception:
                year = None
        if year is None:
            year = datetime.date.today().year

        # If model has a specific_date, return it directly
        if obj.specific_date:
            return obj.specific_date

        # Fixed recurring with month/day
        if obj.is_recurring and obj.month and obj.day:
            try:
                return datetime.date(year, obj.month, obj.day)
            except Exception:
                return None

        # Maundy Thursday, Good Friday, Black Saturday (based on Easter)
        name = (obj.name or '').lower()
        if 'maundy' in name or 'good friday' in name or 'black saturday' in name or 'holy week' in (obj.notes or '').lower():
            try:
                easter = easter_date(year)
                if 'maundy' in name:
                    return easter - datetime.timedelta(days=3)
                if 'good friday' in name:
                    return easter - datetime.timedelta(days=2)
                if 'black' in name:
                    return easter - datetime.timedelta(days=1)
            except Exception:
                return None

        # National Heroes Day: last Monday of August
        if 'national heroes' in name or 'national heroes day' in name:
            try:
                return last_monday_of_august(year)
            except Exception:
                return None

        # Chinese New Year and other lunisolar movable dates: not computed here
        return None

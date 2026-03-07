import re
from datetime import date, datetime

import babel.dates

from odoo.api import Environment
from odoo.exceptions import ValidationError
from odoo.tools import get_lang
from odoo.tools.translate import LazyTranslate

_lt = LazyTranslate("base")


def get_python_babel_format_mapping():
    return {
        "%A": "EEEE",  # Full weekday name
        "%a": "EEE",  # Abbreviated weekday name
        "%w": None,  # Weekday as a number (0=Sunday) – no direct Babel equivalent
        "%d": "dd",  # Day of month, zero-padded
        "%-d": "d",  # Day of month, non-padded (Unix only)
        "%b": "LLL",  # Abbreviated month name
        "%B": "LLLL",  # Full month name
        "%m": "MM",  # Month as zero-padded decimal
        "%-m": "M",  # Month as non-padded decimal (Unix only)
        "%y": "yy",  # Year without century (BE adjustment needed)
        "%Y": "yyyy",  # Full year (BE adjustment needed)
        "%H": "HH",  # Hour (24-hour)
        "%I": "hh",  # Hour (12-hour)
        "%p": "a",  # AM/PM
        "%M": "mm",  # Minute
        "%S": "ss",  # Second
        "%f": None,  # Microsecond – no Babel equivalent
        "%z": "Z",  # UTC offset (limited support)
        "%Z": "z",  # Timezone name
        "%j": "D",  # Day of the year (approximate)
        "%U": None,  # Week number (Sunday-start) – no direct equivalent
        "%W": None,  # Week number (Monday-start) – no direct equivalent
        "%c": "medium",  # Locale's full date and time – use format_datetime
        "%x": "short",  # Locale’s date – use format_date
        "%X": None,  # Locale’s time – use format_time
        "%C": None,  # Century – no Babel equivalent
        "%G": None,  # ISO 8601 year – no Babel equivalent
        "%u": None,  # ISO weekday (1=Mon) – no Babel equivalent
        "%V": None,  # ISO week number – no Babel equivalent
    }


def get_date_only_directives():
    return {"%Y", "%y", "%m", "%b", "%B", "%d", "%a", "%A"}


def get_time_only_directives():
    return {"%H", "%I", "%p", "%M", "%S"}


def extract_directives(date_format):
    """
    Extracts all Python-style format directives from a format string.

    This method scans a format string and returns all directives that start with '%'
    followed by a letter (e.g., "%d", "%Y", "%H").

    Args:
        date_format (str): The format string containing Python-style directives.

    Returns:
        set[str]: A set of format directives found in the input string.

    Example:
        extract_directives("%d/%m/%Y %H:%M") → {'%d', '%m', '%Y', '%H', '%M'}
    """
    return set(re.findall(r"%[a-zA-Z]", date_format))


def _validate_date_format(date_format):
    """
    Validate that a given date format string contains only date-related directives.

    This method extracts all Python-style strftime directives from the provided
    format string (e.g., "%d/%m/%Y") and checks that none of them correspond to
    time-specific elements like hours, minutes, or seconds. If any time directives
    are found in a date-only format, a ValidationError is raised.

    Args:
        date_format (str): A Python-style strftime format string.

    Raises:
        ValidationError: If the format string contains any time-related directives.

    Example:
        Valid: "%d/%m/%Y"
        Invalid: "%d/%m/%Y %H:%M" → raises ValidationError due to %H and %M
    """
    directives = extract_directives(date_format)
    # Checking intersection
    invalid = directives & get_time_only_directives()
    if invalid:
        raise ValidationError(
            _lt(
                f"Invalid format for date object: time directives {invalid} "
                "are not allowed."
            )
        )


def get_locale_date_format(
    env: Environment,
    dt: date | datetime,
    py_format: str = None,
    be_year: bool = False,
    iso_code: str = None,
) -> str:
    """
    Format a `datetime.date` or `datetime.datetime` using the given language locale,
    with optional Buddhist Era year.

    - Converts a Python-style `datetime.date` or `datetime.datetime` format to
        Babel format.
    - Formats the given date/datetime object accordingly
        using the specified locale.
    - Optionally replaces the year with the Buddhist Era (BE) equivalent.

    Only appropriate format codes should be used:
        - If a `datetime.date` object is passed, the format must **not**
            include time-related codes (e.g., "%H", "%M", "%S").
        - If a `datetime.datetime` object is passed, both date and
            time format codes are acceptable.

    Args:
        - dt (date | datetime): A `datetime.date` or `datetime.datetime` object.
        - py_format (str, optional): Python-style date format string.
                                        If not given, defaults user's language format.
        - be_year (bool, optional): If True, replaces year with Buddhist Era (+543).
        - iso_code (str, optional): ISO code (e.g., "th", "en").
                                    Defaults to the current user's language setting.

    Raises:
        - ValueError: If an inappropriate format is used
            (e.g., time format on a `date` object).

    Returns:
        str: The formatted date string.

    Examples:
        date(2024, 5, 6), "%d/%m/%Y", be_year=True, iso_code="th_TH" → '06/05/2567'
        date(2024, 5, 6), "%d-%b-%y", iso_code="en_US" → '06-May-24'
        date(2024, 5, 6)  → '6 พฤษภาคม 2024'  # assuming user's land is Thai
    """

    user_lang = get_lang(env)
    if not iso_code:
        iso_code = user_lang.iso_code

    date_format = py_format or user_lang.date_format

    if isinstance(dt, date) and not isinstance(dt, datetime):
        _validate_date_format(date_format)

    # Convert Python format to Babel format
    for py_code, babel_code in get_python_babel_format_mapping().items():
        if not py_code or not babel_code:
            continue

        date_format = date_format.replace(py_code, babel_code)

    if isinstance(dt, datetime):
        formatted = babel.dates.format_datetime(dt, format=date_format, locale=iso_code)
    else:
        formatted = babel.dates.format_date(dt, format=date_format, locale=iso_code)

    # If Buddhist Era is requested, replace the Gregorian year(s)
    if be_year and ("yyyy" in date_format or "yy" in date_format):
        greg_year = dt.year
        be_year = greg_year + 543

        # Check for full year (%Y) or short year (%y) in the format
        if "yyyy" in date_format:
            short_greg = str(greg_year)
            short_be = str(be_year)
        elif "yy" in date_format:
            short_greg = str(greg_year % 100).zfill(2)
            short_be = str(be_year % 100).zfill(2)

        formatted = formatted.replace(short_greg, short_be)

    return formatted

# ==========================================================
# Gregorian / Julian -> Ethiopian Calendar Display
# Programming I Final Project
# ==========================================================

# ---------------- MONTH NAMES ----------------

gregorian_months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

ethiopian_months = [
    "Meskerem", "Tikimt", "Hidar", "Tahsas",
    "Tir", "Yekatit", "Megabit", "Miazia",
    "Ginbot", "Sene", "Hamle", "Nehase", "Pagume"
]

weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


# ---------------- LEAP YEARS ----------------

def is_gregorian_leap(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def is_julian_leap(year):
    return year % 4 == 0


def is_ethiopian_leap(year):
    return (year + 1) % 4 == 0


# ---------------- DAYS IN MONTH ----------------

def gregorian_month_days(year):

    days = [31, 28, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31]

    if is_gregorian_leap(year):
        days[1] = 29

    return days


def julian_month_days(year):

    days = [31, 28, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31]

    if is_julian_leap(year):
        days[1] = 29

    return days
def ethiopian_month_days(year):

    days = [30, 30, 30, 30, 30, 30, 30,
             30, 30, 30, 30, 30, 5]
    if is_ethiopian_leap(year):
        days[12] = 6

    return days
# ---------------- DAY OF WEEK ----------------
# 0 = Sunday

def gregorian_day_of_week(year, month, day):

    if month < 3:
        month += 12
        year -= 1

    k = year % 100
    j = year // 100

    h = (day + (13 * (month + 1)) // 5 +
         k + k // 4 + j // 4 + 5 * j) % 7

    return (h + 6) % 7


def julian_day_of_week(year, month, day):

    if month < 3:
        month += 12
        year -= 1

    h = (day + (13 * (month + 1)) // 5 +
         year + year // 4 + 5) % 7

    return (h + 6) % 7


# ---------------- GREGORIAN TO ETHIOPIAN ----------------

def gregorian_to_ethiopian(year, month, day):

    new_year_day = 11

    if is_gregorian_leap(year + 1):
        new_year_day = 12

    gregorian_days = gregorian_month_days(year)

    day_of_year = day

    for i in range(month - 1):
        day_of_year += gregorian_days[i]

    if day_of_year >= 255 + (new_year_day - 11):
        eth_year = year - 7
    else:
        eth_year = year - 8

    new_year_threshold = 255 + (new_year_day - 11)

    if day_of_year < new_year_threshold:
       eth_day_of_year = day_of_year + 111
    else:
       eth_day_of_year = day_of_year - new_year_threshold + 1

    # -------- FIXED PAGUME LOGIC --------

    if eth_day_of_year <= 360:
        eth_month = (eth_day_of_year - 1) // 30 + 1
        eth_day = (eth_day_of_year - 1) % 30 + 1

    else:
        eth_month = 13
        eth_day = eth_day_of_year - 360

    return eth_year, eth_month, eth_day

# ---------------- JULIAN TO ETHIOPIAN ----------------

def julian_to_ethiopian(year, month, day):

    # Approximation using offset
    # Julian is 13 days behind Gregorian (modern years)

    g_day = day + 13
    g_month = month
    g_year = year

    g_days = gregorian_month_days(g_year)

    if g_day > g_days[g_month - 1]:
        g_day -= g_days[g_month - 1]
        g_month += 1

        if g_month > 12:
            g_month = 1
            g_year += 1

    return gregorian_to_ethiopian(g_year, g_month, g_day)


# ---------------- ETHIOPIAN MONTH RANGE ----------------
def ethiopian_month_range(year, month, calendar_type):

    found_months = []

    if calendar_type == "G":
        days = gregorian_month_days(year)[month - 1]
    else:
        days = julian_month_days(year)[month - 1]

    for d in range(1, days + 1):

        if calendar_type == "G":
            e = gregorian_to_ethiopian(year, month, d)
        else:
            e = julian_to_ethiopian(year, month, d)

        month_name = ethiopian_months[e[1] - 1]

        if month_name not in found_months:
            found_months.append(month_name)

    return "-".join(found_months)

# ---------------- PRINT CALENDAR ----------------

def print_month(year, month, calendar_type):

    if calendar_type == "G":
        days_in_month = gregorian_month_days(year)[month - 1]
        first_day = gregorian_day_of_week(year, month, 1)

        eth1 = gregorian_to_ethiopian(year, month, 1)
        eth2 = gregorian_to_ethiopian(year, month, days_in_month)

    else:
        days_in_month = julian_month_days(year)[month - 1]
        first_day = julian_day_of_week(year, month, 1)

        eth1 = julian_to_ethiopian(year, month, 1)
        eth2 = julian_to_ethiopian(year, month, days_in_month)

    print()
    print("=" * 58)

    if calendar_type == "G":
        print(f"Gregorian Year: {year}      Ethiopian Years: {eth1[0]} - {eth2[0]}")
    else:
        print(f"Julian Year: {year}         Ethiopian Years: {eth1[0]} - {eth2[0]}")

    print()

    eth_range = ethiopian_month_range(year, month, calendar_type)

    print(f"{gregorian_months[month - 1]}      {eth_range}")

    print("-" * 58)

    for w in weekdays:
        print(f"{w:^8}", end="")
    print()

    print("-" * 58)

    current = 1

    for i in range(6):

        for j in range(7):

            if i == 0 and j < first_day:
                print(" " * 8, end="")

            elif current <= days_in_month:

                if calendar_type == "G":
                    e = gregorian_to_ethiopian(year, month, current)
                else:
                    e = julian_to_ethiopian(year, month, current)
                top = f"{current}"
                bottom = f"{e[2]}"

                print(f"{top:>2}/{bottom:<5}", end=" ")

                current += 1

            else:
                print(" " * 8, end="")

        print()
        print()

        if current > days_in_month:
            break

    print("=" * 58)


# ---------------- PRINT WHOLE YEAR ----------------

def print_year(year, calendar_type):

    for month in range(1, 13):
        print_month(year, month, calendar_type)

def print_year_1752():
    
    for month in range(1, 9):
        print_month(1752, month, "J")

    print_september_1752()

    for month in range(10, 13):
        print_month(1752, month, "G")
# ---------------- MAIN PROGRAM ----------------
def print_september_1752():

    print()
    print("=" * 58)
    print("Julian/Gregorian Transition Year: 1752")
    print("September")
    print("-" * 58)

    for w in weekdays:
        print(f"{w:^8}", end="")
    print()

    print("-" * 58)

    first_day = gregorian_day_of_week(1752, 9, 1)
    days_in_month = gregorian_month_days(1752)[8]

    current = 1

    for i in range(6):
        for j in range(7):

            if i == 0 and j < first_day:
                print(" " * 8, end="")

            elif current <= days_in_month:

                # ✔ ONLY RULE NEEDED
                if 3 <= current <= 13:
                    print(" " * 8, end="")
                else:
                    e = gregorian_to_ethiopian(1752, 9, current)
                    print(f"{current:>2}/{e[2]:<5}", end=" ")

                current += 1

            else:
                print(" " * 8, end="")

        print()
        print()

        if current > days_in_month:
            break

    print("=" * 58)
while True:
   year = int(input("Enter Year: "))
   if year > 1752:
    print_year(year, "G")

   elif year < 1752:
    print_year(year, "J")

   else:
    print_year_1752()

   again = input("\nDo you want to continue? (y/n): ")

   if again.lower() != "y":
     print("Program Ended.")
     break 
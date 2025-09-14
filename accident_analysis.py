import csv
from datetime import datetime
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "US_Accidents_March23.csv"

print("Starting script...")

# Function to load and parse the first 10,000 valid rows
def load_data(limit=10000):
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                start_time = datetime.strptime(row['Start_Time'].split('.')[0], '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime(row['End_Time'].split('.')[0], '%Y-%m-%d %H:%M:%S')
                row['Start_Time_parsed'] = start_time
                row['End_Time_parsed'] = end_time
                row['Hour'] = start_time.hour
                row['Weekday'] = start_time.strftime('%A')
                row['Month'] = start_time.month
                data.append(row)
                if len(data) >= limit:
                    break
            except Exception as e:
                continue
    print(f"Loaded {len(data)} valid rows")
    return data

# ---------- Grade 1: Time of Day Analysis ----------
def grade1(data):
    print("Running Grade 1 - Time of Day Analysis...")
    hours = Counter()
    weekdays = Counter()
    months = Counter()

    for row in data:
        hours[row['Hour']] += 1
        weekdays[row['Weekday']] += 1
        months[row['Month']] += 1

    plt.figure(figsize=(12, 8))

    # Plot 1: Accidents by Hour
    plt.subplot(2, 2, 1)
    hour_keys = sorted(hours.keys())
    hour_values = [hours[k] for k in hour_keys]
    plt.bar(hour_keys, hour_values)
    plt.title('Accidents by Hour of Day')

    # Plot 2: Accidents by Day of Week
    plt.subplot(2, 2, 2)
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_values = [weekdays[w] for w in weekday_order]
    plt.bar(weekday_order, weekday_values)
    plt.xticks(rotation=45)
    plt.title('Accidents by Day of Week')

    # Plot 3: Trend of Accidents by Hour
    plt.subplot(2, 2, 3)
    plt.plot(hour_keys, hour_values)
    plt.title('Trend of Accidents by Hour')

    # Plot 4: Accidents by Month
    plt.subplot(2, 2, 4)
    month_keys = sorted(months.keys())
    month_values = [months[k] for k in month_keys]
    plt.bar(month_keys, month_values)
    plt.title('Accidents by Month')

    plt.tight_layout()
    plt.show()

# ---------- Grade 2: Weather Conditions Analysis ----------
def grade2(data):
    print("Running Grade 2 - Weather Conditions Analysis...")
    weather_counter = Counter()
    temperature_by_severity = defaultdict(list)
    wind_speed_by_severity = defaultdict(list)
    precipitation_by_severity = defaultdict(list)

    for row in data:
        weather = row.get('Weather_Condition', 'Unknown')
        weather_counter[weather] += 1
        try:
            temp = float(row.get('Temperature(F)', 0))
            wind = float(row.get('Wind_Speed(mph)', 0))
            precip = float(row.get('Precipitation(in)', 0))
            severity = int(row.get('Severity', 1))
            temperature_by_severity[severity].append(temp)
            wind_speed_by_severity[severity].append(wind)
            precipitation_by_severity[severity].append(precip)
        except:
            continue

    plt.figure(figsize=(12, 8))

    # Plot 1: Top 10 Weather Conditions
    plt.subplot(2, 2, 1)
    top_weather = weather_counter.most_common(10)
    labels, counts = zip(*top_weather)
    plt.barh(labels, counts)
    plt.title('Top 10 Weather Conditions')

    # Plot 2: Temperature vs Severity
    plt.subplot(2, 2, 2)
    temps = []
    severities = []
    for severity, values in temperature_by_severity.items():
        temps.extend(values)
        severities.extend([severity]*len(values))
    sns.boxplot(x=severities, y=temps)
    plt.title('Temperature vs Severity')

    # Plot 3: Wind Speed vs Severity
    plt.subplot(2, 2, 3)
    winds = []
    severities = []
    for severity, values in wind_speed_by_severity.items():
        winds.extend(values)
        severities.extend([severity]*len(values))
    sns.boxplot(x=severities, y=winds)
    plt.title('Wind Speed vs Severity')

    # Plot 4: Precipitation vs Severity
    plt.subplot(2, 2, 4)
    precs = []
    severities = []
    for severity, values in precipitation_by_severity.items():
        precs.extend(values)
        severities.extend([severity]*len(values))
    sns.boxplot(x=severities, y=precs)
    plt.title('Precipitation vs Severity')

    plt.tight_layout()
    plt.show()

# ---------- Grade 3: Road Conditions and Hotspots ----------
def grade3(data):
    print("Running Grade 3 - Road Conditions and Hotspots...")
    side_counter = Counter()
    amenity_counter = Counter()
    bump_counter = Counter()
    state_counter = Counter()

    for row in data:
        side_counter[row.get('Side', 'Unknown')] += 1
        amenity_counter[row.get('Amenity', 'Unknown')] += 1
        bump_counter[row.get('Bump', 'Unknown')] += 1
        state_counter[row.get('State', 'Unknown')] += 1

    plt.figure(figsize=(12, 8))

    # Plot 1: Side of Road
    plt.subplot(2, 2, 1)
    sides = list(side_counter.keys())
    counts = list(side_counter.values())
    plt.barh(sides, counts)
    plt.title('Side of Road in Accidents')

    # Plot 2: Top 10 Amenities
    plt.subplot(2, 2, 2)
    top_amenities = amenity_counter.most_common(10)
    labels, counts = zip(*top_amenities)
    plt.barh(labels, counts)
    plt.title('Top 10 Amenities Involved')

    # Plot 3: Presence of Bump
    plt.subplot(2, 2, 3)
    bumps = list(bump_counter.keys())
    counts = list(bump_counter.values())
    plt.barh(bumps, counts)
    plt.title('Presence of Bump')

    # Plot 4: Top 10 States
    plt.subplot(2, 2, 4)
    top_states = state_counter.most_common(10)
    labels, counts = zip(*top_states)
    plt.barh(labels, counts)
    plt.title('Top 10 States with Most Accidents')

    plt.tight_layout()
    plt.show()

# ---------- Main function ----------
def main():
    data = load_data(limit=10000)
    grade1(data)
    grade2(data)
    grade3(data)

if __name__ == "__main__":
    main()

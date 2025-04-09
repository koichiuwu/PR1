from collections import defaultdict

class City:
    def __init__(self, x, y, country):
        self.x = x
        self.y = y
        self.country = country
        self.coins = defaultdict(int)
        self.coins[country] = 1000000
        self.new_coins = defaultdict(int)
        self.neighbors = []

    def distribute(self):
        for coin_country, amount in self.coins.items():
            send = amount // 1000
            if send > 0:
                for neighbor in self.neighbors:
                    neighbor.new_coins[coin_country] += send
                
                self.coins[coin_country] -= send * len(self.neighbors)

    def update(self):
        for k, v in self.new_coins.items():
            self.coins[k] += v
        self.new_coins.clear()

    def is_complete(self, all_countries):
        return set(self.coins.keys()) == all_countries

class Country:
    def __init__(self, name, xl, yl, xh, yh):
        self.name = name
        self.cities = []
        for x in range(xl, xh + 1):
            for y in range(yl, yh + 1):
                self.cities.append(City(x, y, name))

    def is_complete(self, all_countries):
        return all(city.is_complete(all_countries) for city in self.cities)

def simulate(countries):
    city_map = {}
    for country in countries:
        for city in country.cities:
            city_map[(city.x, city.y)] = city

    for city in city_map.values():
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = city_map.get((city.x + dx, city.y + dy))
            if neighbor:
                city.neighbors.append(neighbor)

    all_country_names = set(country.name for country in countries)
    completed = {}
    day = 0

    while len(completed) < len(countries):
        for city in city_map.values():
            city.distribute()
        for city in city_map.values():
            city.update()
        day += 1
        for country in countries:
            if country.name not in completed and country.is_complete(all_country_names):
                completed[country.name] = day

    return completed

def main():
    all_cases = [
        [("France", 1, 4, 4, 6), ("Spain", 3, 1, 6, 3), ("Portugal", 1, 1, 2, 2)],
        [("Luxembourg", 1, 1, 1, 1)],
        [("Netherlands", 1, 3, 2, 4), ("Belgium", 1, 1, 2, 2)],
    ]

    for i, case in enumerate(all_cases):
        countries = [Country(name, x1, y1, x2, y2) for name, x1, y1, x2, y2 in case]
        result = simulate(countries)
        print(f"Case Number {i + 1}")
        for name, days in sorted(result.items(), key=lambda x: (x[1], x[0])):
            print(f"{name} {days}")

if __name__ == "__main__":
    main()

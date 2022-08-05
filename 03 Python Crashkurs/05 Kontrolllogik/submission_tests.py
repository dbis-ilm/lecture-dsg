from jptest import *


@JPTest('Aufgabe 1', max_score=2, execute=('task-1',))
def aufgabe1(tb: JPTestBook):
    sort = tb.ref('sort')
    yield all([
        sort(11, 12, 13) == [11, 12, 13],
        sort(11, 13, 12) == [11, 12, 13],
        sort(12, 11, 13) == [11, 12, 13],
        sort(12, 13, 11) == [11, 12, 13],
        sort(13, 11, 12) == [11, 12, 13],
        sort(13, 12, 11) == [11, 12, 13]
    ]), 2


@JPTest('Aufgabe 2', max_score=5, execute=('task-2',))
def aufgabe2(tb: JPTestBook):
    def test(station1, station2):
        # Sonderfälle
        if station1 > station2:
            return test(station2, station1)
        if station1 == station2:
            return 0

        # Zerlege Angabe in Linie und Haltestelle
        line1, stop1 = station1 // 10, station1 % 10
        line2, stop2 = station2 // 10, station2 % 10

        # Grundpreis = 2 Euro
        price = 2

        # benachbarte Haltestellen
        if line1 == line2:
            if stop2 - stop1 == 1:
                price -= 1
        elif station1 == 11 and station2 == 21 or station1 == 11 and station2 == 31:
            price -= 1

        # Innenstadtgrenze
        if stop1 == 1 and stop2 > 1:
            price += 1
        elif stop1 > 1 and stop2 == 1:
            price += 1
        elif stop1 > 1 and stop2 > 1:
            price += 2

        # Endhaltestellen
        if stop1 == 3:
            price += 1
        if stop2 == 3:
            price += 1

        # Preis zurückgeben
        return price

    result = tb.ref('price')

    stations = [11, 12, 13, 21, 22, 23, 31, 32, 33]
    for s1 in stations:
        for s2 in stations:
            if s1 != 33 or s2 != 33:
                yield test(s1, s2) == result(s1, s2), 0.0625

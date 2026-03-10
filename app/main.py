from __future__ import annotations


class Deck:
    def __init__(
        self,
        row: int,
        column: int,
        is_alive: bool = True,
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        is_drowned: bool = False,
    ) -> None:
        r1, c1 = start
        r2, c2 = end
        self.is_drowned = is_drowned
        self.decks = []

        if r1 == r2:
            for col in range(min(c1, c2), max(c1, c2) + 1):
                self.decks.append(Deck(r1, col))
        else:
            for row in range(min(r1, r2), max(r1, r2) + 1):
                self.decks.append(Deck(row, c1))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return ""
        if not deck.is_alive:
            return "Sunk!" if self.is_drowned else "Hit!"
        deck.is_alive = False
        self.is_drowned = all(not d.is_alive for d in self.decks)
        return "Sunk!" if self.is_drowned else "Hit!"


class Battleship:
    def __init__(
        self,
        ships: list[tuple[tuple[int, int], tuple[int, int]]],
    ) -> None:
        self.field = {}
        for start, end in ships:
            ship = Ship(start, end)
            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple[int, int]) -> str:
        if location not in self.field:
            return "Miss!"
        ship = self.field[location]
        row, column = location
        return ship.fire(row, column)

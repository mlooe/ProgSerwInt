from dependency_injector.wiring import Provide

import asyncio

from container import Container
from services.ipost_adress_service import IPostAdressService
from utils import consts


async def main():
    container = Container()
    service = container.service()
    repository = container.repository()

    while True:
        print("""
        Wybierz opcje:
        1 - Pobierz dane współbieżne
        2 - Wyświetl wszystkie posty
        3 - Sortuj posty po czasie ostatniego użycia
        4 - Wyświetl post po indeksie
        5 - Szukaj po tytule/treści lub komentarzu
        6 - Czyszczenie w tle (N sekund)
        0 - Wyjdź 
        """)

        try:
            choice = int(input("Twój wybór: "))
        except ValueError:
            print("Podaj właściwą liczbę!")
            continue

        match choice:
            case 1:
                await service.load_data()

            case 2:
                posts = await repository.get_posts()
                for p in posts:
                    print(p.id, p.title, p.last_used)

            case 3:
                sorted_posts = await service.sort_by_usage()
                for p in sorted_posts:
                    print(p.id, p.title, p.last_used)

            case 4:
                index = int(input("Podaj indeks postu: "))
                posts = await repository.get_posts()
                if 0 <= index < len(posts):
                    p = posts[index]
                    print(p.id, p.title, p.last_used)
                else:
                    print("Zły indeks!")

            case 5:
                filtr = input("Podaj frazę do wyszukania: ")
                found = await service.filter(filtr)
                if not found:
                    print("Brak wyszukiwań")
                else:
                    for p in found:
                        print(p.id, p.title)

            case 6:
                seconds = int(input("Usuń rekordy starsze niż N sekund: "))
                asyncio.create_task(service.cleanup(seconds))

            case 0:
                print("Zamykanie")
                break

            case _:
                print("Zła opcja")

if __name__ == "__main__":
    asyncio.run(main())
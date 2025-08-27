from db import engine, Base, SessionLocal
from models import Author, Book, Genre
from datetime import date

Base.metadata.create_all(bind=engine)

session = SessionLocal()

fiction = Genre(name="Fiction")
fantasy = Genre(name="Fantasy", parent=fiction)
highFantasy = Genre(name="High Fantasy", parent=fantasy)
epicFantasy = Genre(name="Epic Fantasy", parent=highFantasy)
urbanFantasy = Genre(name="Urban Fantasy", parent=fantasy)
scienceFiction = Genre(name="Science Fiction", parent=fiction)
dystopian = Genre(name="Dystopian", parent=scienceFiction)
spaceOpera = Genre(name="Space Opera", parent=scienceFiction)
militarySciFi = Genre(name="Military Sci-Fi", parent=spaceOpera)
mystery = Genre(name="Mystery", parent=fiction)
detective = Genre(name="Detective", parent=mystery)
cozyMystery = Genre(name="Cozy Mystery", parent=mystery)

nonFiction = Genre(name="Non-Fiction")
biography = Genre(name="Biography", parent=nonFiction)
historicalBiography = Genre(name="Historical Biography", parent=biography)
memoir = Genre(name="Memoir", parent=biography)
selfHelp = Genre(name="Self Help", parent=nonFiction)
personalDevelopment = Genre(name="Personal Development", parent=selfHelp)
motivational = Genre(name="Motivational", parent=personalDevelopment)
psychology = Genre(name="Psychology", parent=selfHelp)
history = Genre(name="History", parent=nonFiction)
ancientHistory = Genre(name="Ancient History", parent=history)
modernHistory = Genre(name="Modern History", parent=history)
worldWar2 = Genre(name="World War II", parent=modernHistory)

childrenBook = Genre(name="Children Book")
pictureBook = Genre(name="Picture Book", parent=childrenBook)
bedtimeStory = Genre(name="Bedtime Story", parent=pictureBook)
youngAdult = Genre(name="Young Adult", parent=childrenBook)
youngAdultFantasy = Genre(name="Young Adult Fantasy", parent=youngAdult)
youngAdultRomance = Genre(name="Young Adult Romance", parent=childrenBook)

romance = Genre(name="Romance")
contemporaryRomance = Genre(name="Contemporary Romance", parent=romance)
historicalRomance = Genre(name="Historical Romance", parent=romance)
regencyRomance = Genre(name="Regency Romance", parent=historicalRomance)
victorianRomance = Genre(name="Victorian Romance", parent=historicalRomance)
paranormalRomance = Genre(name="Paranormal Romance", parent=romance)
vampireRomance = Genre(name="Vampire Romance", parent=paranormalRomance)

horror = Genre(name="Horror")
gothicHorror = Genre(name="Gothic Horror", parent=horror)
psychologicalHorror = Genre(name="Psychological Horror", parent=horror)
supernaturalHorror = Genre(name="Supernatural Horror", parent=horror)
ghostStories = Genre(name="Ghost Stories", parent=supernaturalHorror)

genres = [
    fiction, fantasy, highFantasy, epicFantasy, urbanFantasy, scienceFiction, dystopian, spaceOpera, militarySciFi, mystery, detective, cozyMystery, 
    nonFiction, biography, historicalBiography, memoir,selfHelp, personalDevelopment, motivational, psychology, history, ancientHistory, modernHistory, worldWar2, 
    childrenBook, pictureBook, bedtimeStory, youngAdult, youngAdultFantasy, youngAdultRomance, 
    romance, contemporaryRomance, historicalRomance, regencyRomance, victorianRomance, paranormalRomance, vampireRomance, 
    horror, gothicHorror, psychologicalHorror, supernaturalHorror, ghostStories,
]


book1 = Book(title="book1", pub_date=date(2000,10,1), genres=[epicFantasy, psychology])
book2 = Book(title="book2", pub_date=date(2000,10,2), genres=[bedtimeStory, victorianRomance, paranormalRomance])
book3 = Book(title="book3", pub_date=date(2000,10,3), genres=[urbanFantasy, scienceFiction, ancientHistory])
book4 = Book(title="book4", pub_date=date(2000,10,4), genres=[ancientHistory, scienceFiction, nonFiction])
book5 = Book(title="book5", pub_date=date(2000,10,5), genres=[epicFantasy, psychology, selfHelp, memoir])
book6 = Book(title="book6", pub_date=date(2000,10,6), genres=[epicFantasy, psychology, ancientHistory, modernHistory])
book7 = Book(title="book7", pub_date=date(2000,10,7), genres=[epicFantasy, psychology, contemporaryRomance, supernaturalHorror, ghostStories])
book8 = Book(title="book8", pub_date=date(2000,10,8), genres=[epicFantasy, psychology, biography, dystopian])
book9 = Book(title="book9", pub_date=date(2000,10,9), genres=[childrenBook, psychology, personalDevelopment, militarySciFi])

books = [
    book1, book2, book3, book4, book5, book6, book7, book8, book9
]

author1 = Author(name="author1", b_day=date(2010,8, 11), books=[book5, book6])
author2 = Author(name="author2", b_day=date(2010,8, 12), books=[book1, book8])
author3 = Author(name="author3", b_day=date(2010,8, 13), books=[book2, book9, book7])
author4 = Author(name="author4", b_day=date(2010,8, 14), books=[book9, book3])
author5 = Author(name="author5", b_day=date(2010,8, 15), books=[book2, book6, book5])
author6 = Author(name="author6", b_day=date(2010,8, 16), books=[book4, book8, book3])
author7 = Author(name="author7", b_day=date(2010,8, 17), books=[book5, book6])
author8 = Author(name="author8", b_day=date(2010,8, 18), books=[book5, book4])
author9 = Author(name="author9", b_day=date(2010,8, 19), books=[book8, book2])

authors = [
    author1, author2, author3, author4, author5, author6, author7, author8, author9
]

session.add_all(genres)
session.add_all(books)
session.add_all(authors)
session.commit()
session.close()
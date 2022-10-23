from dotenv import load_dotenv

from transform import Filmwork, Person

load_dotenv()


def main():
    from extract import PostgresExtractor
    extractor = PostgresExtractor()

    for data in extractor.extract():
        for row in data:
            print(row)

if __name__ == '__main__':
    main()

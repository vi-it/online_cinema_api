from dotenv import load_dotenv

import transform


load_dotenv()


def main():
    from extract import PostgresExtractor
    extractor = PostgresExtractor()

    for data in extractor.extract():
        for row in data:
            data = transform.Transform(row)
            film = data.to_filmwork()
            print(dict(film))

if __name__ == '__main__':
    main()

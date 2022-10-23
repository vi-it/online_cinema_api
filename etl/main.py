from dotenv import load_dotenv


load_dotenv()


def main():
    from extract import PostgresExtractor
    extractor = PostgresExtractor()

    for data in extractor.extract():
        print(data)

if __name__ == '__main__':
    main()

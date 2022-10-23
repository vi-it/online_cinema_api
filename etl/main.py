from dotenv import load_dotenv

import transform
import upload


load_dotenv()


def main():
    from extract import PostgresExtractor
    extractor = PostgresExtractor()

    counter = 0
    for raw_data in extractor.extract(chunk=10):
        for row in raw_data:
            counter += 1
            fw = transform.Transform(row)
            film = fw.to_filmwork()

            import json
            with open('testing', 'a') as file:
                file.write(json.dumps(dict(film)))
                file.write('\n')

            es_loader = upload.ElasticsearchLoader()
            es_loader.upload_data(film)
    print(counter)

if __name__ == '__main__':
    main()

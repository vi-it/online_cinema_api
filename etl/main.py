from dotenv import load_dotenv

import transform
import upload
from extract import PostgresExtractor


load_dotenv()


class PostgresToElastic:

    def process_data(self):
        extractor = PostgresExtractor()

        for raw_data in extractor.extract():
            for row in raw_data:
                fw = transform.Transform(row)
                film = fw.to_filmwork()

                es_loader = upload.ElasticsearchLoader()
                es_loader.upload_data(film)


def main():
   pg_to_es = PostgresToElastic()
   pg_to_es.process_data()


if __name__ == '__main__':
    main()

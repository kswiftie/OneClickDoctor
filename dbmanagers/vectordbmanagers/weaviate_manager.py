import weaviate, time, logging
from adodbapi import DataError
from weaviate.classes.config import Configure, Property
from weaviate.exceptions import WeaviateConnectionError


class WManager:
    def __init__(self, loading_max_time: int = 30):
        self.logger = logging.getLogger(__name__)
        self.failed_objects: list = []
        start = time.time()

        while time.time() - start < loading_max_time:
            try:
                self.client = weaviate.connect_to_local()
                return
            except Exception:
                time.sleep(1)
        raise WeaviateConnectionError("Couldnt connect to weaviate")

    def __del__(self):
        self.client.close()

    def create_collection(
        self,
        name: str,
        properties: list[Property],
        vec_config,
    ) -> None:
        self.client.collections.create(
            name=name,
            properties=properties,
            vectorizer_config=[
                Configure.NamedVectors.text2vec_transformers(**vec_config)
            ],
        )

    def get_data(self, collection_name: str, limit: int = 10):

        cur_collection = self.client.collections.get(collection_name)
        return [
            obj.properties
            for obj in cur_collection.query.fetch_objects(limit=limit).objects
        ]

    def search_near_data(
        self, collection_name: str, input_data: str, count_of_neighbours: int = 5
    ):
        cur_collection = self.client.collections.get(collection_name)

        return [
            obj.properties
            for obj in cur_collection.query.near_text(
                query=input_data, limit=count_of_neighbours
            ).objects
        ]

    def add_data(
        self,
        collection_name: str,
        input_data,
        batch_size: int = 200,
        max_errors: int = 10,
    ) -> tuple[int, list]:
        try:
            collection = self.client.collections.get(collection_name)
        except Exception as e:
            self.logger.error(f"Couldnt get the collections {collection_name}: {e}")
            raise DataError(f"Collection fetch failed: {e}")

        success_count = 0
        failed = []

        with collection.batch.fixed_size(batch_size=batch_size) as batch:
            for obj in input_data:
                try:
                    batch.add_object(properties=obj)
                except Exception as e:
                    self.logger.warning(f"Couldnt add the object {obj}: {e}")
                if batch.number_errors > max_errors:
                    raise DataError(
                        f"Batch import stopped: exceeded {max_errors} errors."
                    )

            failed = collection.batch.failed_objects.copy()
            success_count = len(list(input_data)) - len(failed)

        self.logger.info(
            f"Added objects to collection {collection_name}: {success_count}, "
            f"Couldnt add: {len(failed)}"
        )
        self.failed_objects = failed
        return success_count, failed

    def look_at_failed_objects(self, count_of_files_to_print: int = 15):
        """
        CALL THIS AFTER U USED METHOD  ADD_DATA
        :return:
        """
        if not self.failed_objects:
            raise RuntimeError("Function were called before method add_data")

        if self.failed_objects:
            print(f"Number of failed imports: {len(self.failed_objects)}")
            print(f"First failed object:")
            print(*self.failed_objects[:count_of_files_to_print], sep="\n")

    def delete_collection(self, collection_name: str) -> None:
        self.client.collections.delete(collection_name)

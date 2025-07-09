from dbmanagers.vectordbmanagers.weaviate_manager import WManager
from weaviate.classes.config import Property, DataType

vectorizer_config = {
    "name": "vectorizer",
    "source_properties": ["symptoms"],
}

medical_properties = [
    Property(name="symptoms", data_type=DataType.TEXT, description="Patient symptoms"),
    Property(
        name="doctors",
        data_type=DataType.TEXT_ARRAY,
        description="Doctors that may help with such symptoms",
    ),
    Property(
        name="Diagnosis",
        data_type=DataType.TEXT,
        description="Diagnosis according to symptoms",
    ),
]

wm = WManager()
wm.create_collection(
    name="SymptomDisease", properties=medical_properties, vec_config=vectorizer_config
)

from app.transformers import transformer_service1, transformer_service2


class TransformFactory:
    transformers = {
        'transformer_service1': transformer_service1,
        'transformer_service2': transformer_service2,
    }
    @classmethod
    def get_transformer(cls, transformer_name: str):
        if transformer_name not in cls.transformers:
            raise ValueError(f"Unknown transformer: {transformer_name}")
        return cls.transformers[transformer_name]

    @classmethod
    def transform_message(cls, transformer_name: str, record: dict):
        transformer = cls.get_transformer(transformer_name)
        return transformer.to_external(record)
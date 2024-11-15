class Global:
    attributes: dict = {}
    
    @classmethod
    def set(cls, key: str, value: any):
        cls.attributes[key] = value
    
    @classmethod
    def get(cls, key: str, default: any) -> any:
        return cls.attributes.get(key, default)

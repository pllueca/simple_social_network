class ServiceError(Exception):
    pass


class ResourceMissingError(ServiceError):
    pass

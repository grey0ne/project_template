from typing import Any

from storages.backends.s3 import S3Storage  # type: ignore


def replace_domain(url: str, domain: str, protocol: str) -> str:
    result = url.split('//', 1)[-1]
    result = result.split('/', 1)[-1]
    return f'{protocol}//{domain}/{result}'


class CustomS3Storage(S3Storage):
    def __init__(self, domain: str, url_protocol: str = 'https:', *args: Any, **kwargs: Any) -> None:
        self.domain = domain
        self.url_protocol = url_protocol
        super().__init__(*args, **kwargs)  # type: ignore

    def url(
        self,
        name: str,
        parameters: Any = None,
        expire: int | None = None,
        http_method: str | None = None,
    ) -> str:
        if not name:
            return name # return empty string if name is empty
        base_url = super().url(name, parameters, expire, http_method) # type: ignore
        url = replace_domain(
            url=base_url, # type: ignore
            domain=self.domain,
            protocol=self.url_protocol
        )
        return url

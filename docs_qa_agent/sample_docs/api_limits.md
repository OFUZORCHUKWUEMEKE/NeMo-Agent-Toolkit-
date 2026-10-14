# API Rate Limits

The public API allows 100 requests per minute per API key on the Standard tier and 1000 requests per minute on the Enterprise tier.

When a limit is exceeded the API returns HTTP 429 with a Retry-After header. Clients should back off and retry after the number of seconds given.

API keys can be rotated from Settings > Developer > API keys. Old keys stop working immediately after rotation.

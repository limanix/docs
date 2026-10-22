[![limanix.dev](https://img.shields.io/website?url=https%3A%2F%2Flimanix.dev&label=limanix.dev&up_message=online)](https://limanix.dev)
[![docs.limanix.dev](https://img.shields.io/website?url=https%3A%2F%2Fdocs.limanix.dev&label=docs.limanix.dev&up_message=online)](https://docs.limanix.dev)
[![License: Apache-2.0](https://img.shields.io/github/license/limanix/docs?label=license)](LICENSE)

<p align="center">
  <img src=".github/assets/readme-header.png"
       alt="LimaNix"
       width="100%">
</p>

The website and documentation of [LimaNix](https://github.com/limanix/client):
NixOS development machines on your Mac, declared in one file.

[Website](https://limanix.dev) |
[Docs](https://docs.limanix.dev) |
[Client](https://github.com/limanix/client) |
[Modules](https://github.com/limanix/modules) |
[lmx](https://github.com/limanix/lmx)

## Development

| Path    | Contents                                  |
| ------- | ----------------------------------------- |
| `site/` | limanix.dev, a Vue app                    |
| `docs/` | docs.limanix.dev, a VitePress site        |
| `tf/`   | The hosting: S3 buckets behind CloudFront |

Run a site locally with [Task](https://taskfile.dev) and Docker:

```console
task run/site    # http://localhost:5173
task run/docs    # http://localhost:5174
```

## Contributing

Follow the
[contribution guide](https://github.com/limanix/.github/blob/main/CONTRIBUTING.md).
Licensed under [Apache 2.0](LICENSE).

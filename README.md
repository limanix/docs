# LimaNix documentation

The LimaNix documentation website.

## Local preview

Requires [Task](https://taskfile.dev/) 3.53.1 or newer and Docker.
Python and uv run in the pinned shared container; documentation dependencies are installed from `uv.lock`.

```console
task --yes docs/serve
```

Open <http://127.0.0.1:8070/>. 
Changes to the pages or Sphinx configuration rebuild the site automatically. 
Stop the preview with `Ctrl+C`.

To use another port:

```console
task --yes docs/serve DOCS_PORT=8071
```

### Include local projects

Pass project directories in `DOCS`:

```console
task --yes docs/serve DOCS='../modules'
```

For several projects:

```console
task --yes docs/serve DOCS='../modules ../client'
```

Each directory must contain `docs/index.md`. Relative paths are resolved from
this repository. Use absolute paths for projects elsewhere; quote a path inside
the list when it contains spaces:

```console
task --yes docs/serve DOCS='../modules "/path/to/my client"'
```

The homepage and sidebar gain a **Local projects** section. Each project uses
its directory name for a separate URL, such as `/projects/modules/index.html`.
Names are lowercased; letters, digits, underscores, and hyphens are kept. Other
characters become hyphens. Project names must remain distinct after this conversion.

The preview uses this site's Sphinx configuration. It copies each complete
`docs/` tree, including images and downloadable examples, into a temporary
directory. Keep relative links and included files inside that tree. A project's
own `conf.py`, theme, or dependencies are not loaded.

Edits, new pages, and deleted pages trigger a rebuild. Site configuration and
static assets are watched too. Project directories are mounted read-only; the
preview does not modify their documentation. Restart the command to change the
project list. `DOCS_PORT` works with `DOCS`.

## Build

```console
task --yes ci/docs
```

The AWS S3 and CloudFront infrastructure configuration is in [`tf/`](tf/).

## Infrastructure

Terraform follows the original Limanix site's private S3 and CloudFront setup.
It pins Terraform `1.15.9` and the AWS provider `6.57.1`; the tasks use the shared
Terraform container.

The values selected for `limanix.dev` are:

| Parameter | Value |
|-----------|-------|
| Site hostname | `limanix.dev` |
| Site bucket | `limanix-prod-docs` |
| AWS region | `us-east-1` |
| State bucket | `tfstates-limanix` |
| State key | `docs/production/terraform.tfstate` |
| State region | `us-east-1` |

These are configuration values, not a deployment record. The state bucket name
is selected for later creation; this Terraform configuration does not create it.
Its name differs from the original site's `tfstates-mr-chelyshkin` bucket.

Check the configuration without AWS credentials or the state bucket:

```console
task --yes ci/terraform-fmt
task --yes ci/terraform-validate
```

Before planning, create the state bucket separately and supply AWS credentials
through `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN`
when using temporary credentials. Supply an issued ACM certificate covering
`limanix.dev` in `us-east-1`:

```sh
export TF_STATE_BUCKET='tfstates-limanix'
export TF_STATE_KEY='docs/production/terraform.tfstate'
export TF_STATE_REGION='us-east-1'
export TF_VAR_aws_region='us-east-1'
export TF_VAR_domain_name='limanix.dev'
export TF_VAR_site_bucket_name='limanix-prod-docs'
export TF_VAR_acm_certificate_arn='<issued-certificate-arn>'

task --yes ci/terraform-plan
```

The plan task enables state encryption and S3 lock files. Terraform configures
the site bucket with public access blocked, encryption, versioning, and CloudFront
read access through Origin Access Control. CloudFront redirects HTTP to HTTPS.
Directory URLs ending in `/` resolve to `index.html`; Sphinx `.html` links and
assets keep their paths. The content security policy permits the configured
Mermaid scripts from jsDelivr. Origin errors retain their status because the
current Sphinx build does not generate a custom `404.html`.

DNS records, the ACM certificate, and deployment credentials remain external,
as in the original setup. Terraform outputs the site bucket, CloudFront
distribution ID, domain name, and hosted zone ID for publication and DNS setup.

## Workflows

- `pr.yml` checks the PR label, builds the site, and reports `gate`.

# TerraRisk Policy Bundle

This bundle provides deny-by-default authorization controls for the TerraRisk Agent.

* `opa_bundle/policy.rego` – primary enforcement policy covering mode gating, budget checks, and PII restrictions.
* Future policies should model per-tool approvals and proxy mediation for Windows MCP alignment.

Policies are mounted into OPA by `docker-compose.yml` and are hot-reloaded thanks to the `--watch` flag.

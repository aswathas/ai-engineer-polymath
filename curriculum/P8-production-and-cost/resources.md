# Production and Cost resources

## Must read

- *Site Reliability Engineering*, the Google SRE book - chapters on monitoring, on
  service level objectives and on error budgets. Free, and written for teams of the size
  yours actually is.
  https://sre.google/sre-book/table-of-contents/
- The OpenTelemetry documentation - the getting-started guides and the semantic
  conventions. This is what makes your traces carry meaning instead of adjectives.
  https://opentelemetry.io/
- *Designing Data-Intensive Applications*, Kleppmann - the chapters on monitoring and on
  the cost of what you build.
  https://dataintensive.net/
- The Twelve-Factor App, section 9 on disposability and section 11 on logs - two short
  pages that decide whether a rollback is a five-minute action.
  https://12factor.net/

## Watch

- "Monitoring Distributed Systems", Rob Ewans - a short book on why dashboards without
  a question attached are decoration.
- The OpenCost documentation - read it to understand how cost attribution actually
  happens inside a cluster, then build your own simpler version.
  https://opencost.io/
- The Kubernetes production best practices talks - not the API tour; the sections on
  probes, on resources and on graceful shutdown.

## Skip

- Multi-region active-active and global load balancing - one host, one container and one
  rollback teach the module. Scale is a later problem and a later module.
- Service mesh, eBPF-based observability and bespoke agents - the standard three signals
  are enough to pass the gate.
- Vendor cost-optimisation product tours - the cost model you build is the deliverable,
  not the tool that would have built it.

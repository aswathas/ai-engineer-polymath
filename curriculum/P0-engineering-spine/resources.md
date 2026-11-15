# Engineering Spine resources

## Must read

- *Designing Data-Intensive Applications*, Martin Kleppmann - the chapters on reliability,
  transactions and idempotency; read them before you write the retry wrapper.
  https://dataintensive.net/
- The PostgreSQL documentation on transactions and isolation levels - the behaviour of
  `SERIALIZABLE` versus `READ COMMITTED` decides how you write the double-write test.
  https://www.postgresql.org/docs/
- *The Pragmatic Programmer*, Andrew Hunt and David Thomas - the chapters on tests and
  on "your code as a legacy codebase"; this is where "a real test suite" comes from.
- The Python typing specification - the rules for narrowing and for generics are what make
  the strict-mode type check possible without `Any` on the boundary.
  https://typing.python.org/

## Watch

- The "Rules of Machine Learning" talk series from Google - short, practical, and the
  first episode is the closest thing to a briefing for this module's attitude.
  https://developers.google.com/machine-learning/guides/rules-of-ml
- *Site Reliability Engineering*, the free Google SRE book - read chapter 4 on
  cascading failures before you design the backoff.
  https://sre.google/sre-book/table-of-contents/
- The Twelve-Factor App - read it once, then forget the parts about backing services you
  do not have. The config section is the one that bites.
  https://12factor.net/

## Skip

- Kubernetes, Helm and service meshes - the module runs on one machine, and deployment
  mechanics arrive properly in P8.
- ORM feature tours - you need migrations and constraints, not a query builder.
- Kafka, gRPC and message brokers - one unreliable HTTP dependency teaches the same
  lesson with less to install.

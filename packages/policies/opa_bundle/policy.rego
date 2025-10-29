package terrarisk.authz

default allow := false

deny[msg] {
  not input.request
  msg := "missing request context"
}

allow {
  input.request.mode == "offline"
  allowed_offline_action[input.request.action]
}

allow {
  input.request.actor.role == "admin"
}

deny[msg] {
  input.request.action == "earth_ai.run"
  not input.context.flags.earth_ai_enabled
  msg := "earth_ai access disabled"
}

deny[msg] {
  input.request.cost.estimated > input.context.budget.remaining
  msg := sprintf("insufficient budget for %s", [input.request.action])
}

deny[msg] {
  input.request.scope.geo_precision == "address"
  not input.context.pii_unlocked
  msg := "fine-grained PII access denied"
}

allowed_offline_action := {
  "nri.load",
  "analysis.generate_report",
  "portfolio.offline_demo"
}

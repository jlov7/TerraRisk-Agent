from terrarisk.connectors.bigquery_ee import _infer_bigquery_scalar_type


def test_infer_bigquery_scalar_type_handles_common_values():
    assert _infer_bigquery_scalar_type(True) == "BOOL"
    assert _infer_bigquery_scalar_type(42) == "INT64"
    assert _infer_bigquery_scalar_type(3.14) == "FLOAT64"
    assert _infer_bigquery_scalar_type("string") == "STRING"

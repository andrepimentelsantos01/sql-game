from typing import Any

from app.schemas import RoundResult
from app.services.scenario_service import get_database_path
from app.services.sql_runner import QueryRejectedError, run_select_query


def _normalize(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 6)
    return value


def _normalized_rows(rows: list[list[Any]]) -> list[list[Any]]:
    return [[_normalize(value) for value in row] for row in rows]


def validate_submission(scenario: dict[str, Any], user_query: str) -> RoundResult:
    database_path = get_database_path(scenario)
    try:
        expected = run_select_query(database_path, scenario["expected_sql"])
        user_result = run_select_query(database_path, user_query)
    except QueryRejectedError as exc:
        return RoundResult(
            correct=False,
            message=str(exc),
            user_result=None,
            hint=scenario.get("hint"),
        )

    correct = _normalized_rows(user_result.rows) == _normalized_rows(expected.rows)
    if correct:
        message = "Boa! O resultado retornado bate com a resposta esperada."
        hint = None
    else:
        message = "Ainda não bateu com o resultado esperado. Confira filtros, agrupamentos e ordenação."
        hint = scenario.get("hint")

    return RoundResult(correct=correct, message=message, user_result=user_result, hint=hint)

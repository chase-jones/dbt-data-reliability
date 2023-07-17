from pathlib import Path

from elementary.clients.dbt.dbt_runner import DbtRunner

PATH = Path(__file__).parent.parent / "dbt_project"
MODELS_DIR_PATH = PATH / "models"

_DEFAULT_VARS = {
    "disable_dbt_invocation_autoupload": True,
    "disable_dbt_artifacts_autoupload": True,
    "disable_run_results": True,
}


def get_dbt_runner(target: str) -> DbtRunner:
    return DbtRunner(
        str(PATH),
        target=target,
        vars=_DEFAULT_VARS,
        raise_on_failure=False,
    )

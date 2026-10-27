"""Keep public-image repair separate from an already published package version."""

from fnmatch import fnmatchcase
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTAINER_PATHS = [
    ".github/workflows/container-release.yml",
    "tests/test_publication_workflow.py",
]


def _workflow(name):
    return yaml.safe_load((ROOT / ".github/workflows" / name).read_text())


def test_public_image_refresh_uses_existing_guarded_renderer():
    workflow = _workflow("container-release.yml")
    assert workflow[True]["push"] == {"branches": ["main"], "paths": CONTAINER_PATHS}
    job = workflow["jobs"]["publish-docker"]
    assert (
        job["uses"]
        == "Knuckles-Team/pipelines/.github/workflows/container_pipeline.yml@main"
    )
    assert job["with"] == {"render_connector": True}
    assert not job.get("continue-on-error", False)
    assert "if" not in job
    assert workflow["permissions"] == {"contents": "read"}


def test_real_package_releases_keep_the_existing_success_dependency():
    workflow = _workflow("pipeline.yml")
    jobs = workflow["jobs"]
    assert jobs["publish-pypi"]["uses"].endswith("/python_pipeline.yml@main")
    assert jobs["publish-docker"]["needs"] == "publish-pypi"
    assert jobs["publish-docker"]["with"] == {"render_connector": True}
    assert workflow[True]["push"]["paths-ignore"] == CONTAINER_PATHS


@pytest.mark.parametrize(
    "paths, publishes",
    [
        ([".github/workflows/container-release.yml"], False),
        (["tests/test_publication_workflow.py"], False),
        ([".github/workflows/container-release.yml", "pyproject.toml"], True),
        (
            ["tests/test_publication_workflow.py", "uptime_kuma_agent/mcp_server.py"],
            True,
        ),
        (["uv.lock"], True),
        ([".github/workflows/pipeline.yml"], True),
    ],
)
def test_only_image_contract_changes_skip_duplicate_package_upload(paths, publishes):
    ignores = _workflow("pipeline.yml")[True]["push"]["paths-ignore"]
    actual = any(
        not any(fnmatchcase(path, pattern) for pattern in ignores) for path in paths
    )
    assert actual is publishes

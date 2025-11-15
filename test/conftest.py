# Python standard library
import shutil
import tempfile
from pathlib import Path

# 3rd party
import pytest
from alembic import command
from alembic.config import Config


@pytest.fixture(scope="class", autouse=True)
def migrate_test_db():
    root = Path(__file__).resolve().parent
    alembic_ini = root / "alembic.ini"

    alembic_cfg = Config(str(alembic_ini))

    # We don't want to create real migration files during tests
    # so create a temporary directory for generated revisions.
    tmp_versions = Path(tempfile.mkdtemp())
    alembic_cfg.set_main_option("version_locations", str(tmp_versions))

    # 0. Migrate models
    command.revision(alembic_cfg, autogenerate=True)

    # 1. Upgrade to latest migration
    command.upgrade(alembic_cfg, "head")

    # Run tests
    yield

    # 2. Downgrade back to base
    command.downgrade(alembic_cfg, "base")

    # Cleanup temp folder
    shutil.rmtree(tmp_versions)

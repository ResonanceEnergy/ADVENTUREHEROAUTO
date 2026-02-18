import sys
import subprocess
import logging
from pathlib import Path

import run


def test_help_contains_new_flags():
    proc = subprocess.run([sys.executable, "run.py", "--help"], capture_output=True, text=True)
    assert "--dry-run" in proc.stdout
    assert "--log-file" in proc.stdout
    assert proc.returncode == 0


def test_dry_run_validate_logs_and_returns_zero(capsys):
    ret = run.main(["-v", "--dry-run", "validate"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "would run: validators.run_all()" in captured.err


def test_log_file_created(tmp_path):
    logfile = tmp_path / "cli.log"
    ret = run.main(["-v", "--dry-run", "--log-file", str(logfile), "validate"])
    assert ret == 0
    assert logfile.exists()
    content = logfile.read_text()
    assert "would run" in content or "validators.run_all" in content


def test_generate_dry_run_logs_all_steps(capsys):
    ret = run.main(["-v", "--dry-run", "generate", "--season", "1", "--episode", "2"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "episode_gen.generate" in captured.err
    assert "artbrief_gen.generate" in captured.err
    assert "prompt_gen.generate" in captured.err


def test_validate_executes_validators_module(capsys):
    import importlib
    from tools import validators
    importlib.reload(validators)
    validators.called = False

    ret = run.main(["validate"])
    assert ret == 0
    assert validators.called
    captured = capsys.readouterr()
    assert "validators.run_all executed" in captured.out


def test_generate_executes_all_modules(capsys):
    import importlib
    from tools import episode_gen, artbrief_gen, prompt_gen
    importlib.reload(episode_gen)
    importlib.reload(artbrief_gen)
    importlib.reload(prompt_gen)

    episode_gen.last_args = None
    artbrief_gen.last_args = None
    prompt_gen.last_args = None

    ret = run.main(["generate", "--season", "2", "--episode", "3"])
    assert ret == 0
    assert episode_gen.last_args == (2, 3)
    assert artbrief_gen.last_args == (2, 3)
    assert prompt_gen.last_args == (2, 3)


def test_runall_executes_everything(capsys):
    import importlib
    from tools import bootstrap, validators, episode_gen, artbrief_gen, prompt_gen, imagine_api, asset_tools, unity
    for m in (bootstrap, validators, episode_gen, artbrief_gen, prompt_gen, imagine_api, asset_tools, unity):
        importlib.reload(m)

    bootstrap.called = False
    validators.called = False
    episode_gen.last_args = None
    artbrief_gen.last_args = None
    prompt_gen.last_args = None
    imagine_api.last_args = None
    asset_tools.last_args = None
    unity.called = False

    ret = run.main(["runall"])
    assert ret == 0
    assert bootstrap.called
    assert validators.called
    assert episode_gen.last_args == (1, 1)
    assert artbrief_gen.last_args == (1, 1)
    assert prompt_gen.last_args == (1, 1)
    assert imagine_api.last_args == (1, 1)
    assert asset_tools.last_args == (1, 1)
    assert unity.called

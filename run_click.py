#!/usr/bin/env python3
"""Click-based CLI for Adventure Hero automation.
This module contains the Click command group and preserves the `main(argv)`
entrypoint for backwards compatibility with tests.
"""
from __future__ import annotations

import importlib
import logging
from pathlib import Path
import click

ROOT = Path(__file__).resolve().parent
LOG = logging.getLogger("adventurehero")


def configure_logging(verbosity: int, log_file: str | None = None) -> None:
    level = logging.WARNING
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO

    handler = logging.StreamHandler()
    fmt = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    LOG.handlers.clear()
    LOG.addHandler(handler)
    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(logging.Formatter(fmt))
        LOG.addHandler(fh)
    LOG.setLevel(level)


def call_and_handle(module_name: str, func_name: str, *args, **kwargs):
    LOG.debug("Importing %s.%s", module_name, func_name)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    LOG.info("Starting: %s.%s(%s)", module_name, func_name, ", ".join(map(str, args)))
    return func(*args, **kwargs)


@click.group()
@click.option("-v", "--verbose", count=True, help="Increase verbosity (repeat for more)")
@click.option("--dry-run", is_flag=True, default=False, help="Preview actions without running external tools")
@click.option("--log-file", type=click.Path(), default=None, help="Write logs to the given file (in addition to stdout)")
@click.pass_context
def cli(ctx, verbose: int, dry_run: bool, log_file: str | None):
    configure_logging(verbose, log_file)
    ctx.ensure_object(dict)
    ctx.obj["dry_run"] = dry_run
    ctx.obj["verbose"] = verbose
    ctx.obj["log_file"] = log_file


@cli.command()
@click.pass_context
def bootstrap(ctx):
    if ctx.obj["dry_run"]:
        LOG.info("(dry-run) would run: bootstrap.run()")
    else:
        call_and_handle("tools.bootstrap", "run")


@cli.command()
@click.pass_context
def validate(ctx):
    if ctx.obj["dry_run"]:
        LOG.info("(dry-run) would run: validators.run_all()")
    else:
        call_and_handle("tools.validators", "run_all")


@cli.command()
@click.option("--season", required=True, type=int)
@click.option("--episode", required=True, type=int)
@click.pass_context
def generate(ctx, season: int, episode: int):
    if ctx.obj["dry_run"]:
        LOG.info("(dry-run) would run: episode_gen.generate(%s, %s)", season, episode)
        LOG.info("(dry-run) would run: artbrief_gen.generate(%s, %s)", season, episode)
        LOG.info("(dry-run) would run: prompt_gen.generate(%s, %s)", season, episode)
    else:
        call_and_handle("tools.episode_gen", "generate", season, episode)
        call_and_handle("tools.artbrief_gen", "generate", season, episode)
        call_and_handle("tools.prompt_gen", "generate", season, episode)


@cli.command()
@click.option("--season", required=True, type=int)
@click.option("--episode", required=True, type=int)
@click.pass_context
def imagine(ctx, season: int, episode: int):
    if ctx.obj["dry_run"]:
        LOG.info("(dry-run) would run: imagine_api.run_batch(%s, %s)", season, episode)
    else:
        call_and_handle("tools.imagine_api", "run_batch", season, episode)


@cli.command()
@click.option("--season", required=True, type=int)
@click.option("--episode", required=True, type=int)
@click.pass_context
def postprocess(ctx, season: int, episode: int):
    if ctx.obj["dry_run"]:
        LOG.info("(dry-run) would run: asset_tools.postprocess(%s, %s)", season, episode)
    else:
        call_and_handle("tools.asset_tools", "postprocess", season, episode)


@cli.command()
@click.option("--target", required=True, type=click.Choice(["ios"]))
@click.pass_context
def build(ctx, target: str):
    if target == "ios":
        if ctx.obj["dry_run"]:
            LOG.info("(dry-run) would run: unity.build_ios()")
        else:
            call_and_handle("tools.unity", "build_ios")
    else:
        raise click.UsageError("unsupported build target")


@cli.command()
@click.pass_context
def runall(ctx):
    if ctx.obj["dry_run"]:
        LOG.info("(dry-run) would run: bootstrap.run()")
        LOG.info("(dry-run) would run: validators.run_all()")
        LOG.info("(dry-run) would run: episode_gen.generate(1, 1)")
        LOG.info("(dry-run) would run: artbrief_gen.generate(1, 1)")
        LOG.info("(dry-run) would run: prompt_gen.generate(1, 1)")
        LOG.info("(dry-run) would run: imagine_api.run_batch(1, 1)")
        LOG.info("(dry-run) would run: asset_tools.postprocess(1, 1)")
        LOG.info("(dry-run) would run: unity.build_ios()")
    else:
        call_and_handle("tools.bootstrap", "run")
        call_and_handle("tools.validators", "run_all")
        call_and_handle("tools.episode_gen", "generate", 1, 1)
        call_and_handle("tools.artbrief_gen", "generate", 1, 1)
        call_and_handle("tools.prompt_gen", "generate", 1, 1)
        call_and_handle("tools.imagine_api", "run_batch", 1, 1)
        call_and_handle("tools.asset_tools", "postprocess", 1, 1)
        call_and_handle("tools.unity", "build_ios")


def main(argv: list[str] | None = None) -> int:
    try:
        cli.main(args=argv, standalone_mode=False)
        return 0
    except click.ClickException as e:
        LOG.error(str(e))
        return 2
    except KeyboardInterrupt:
        LOG.warning("Interrupted by user")
        return 130
    except Exception:
        LOG.exception("Command failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
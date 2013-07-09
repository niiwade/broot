# Copyright 2013 Daniel Narvaez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import os
import sys

from broot.root import Root


def create(config, mirror=None):
    root = Root(config)
    root.create(mirror)


def update(config):
    root = Root(config)
    root.update()


def clean(config):
    root = Root(config)
    root.clean()


def run(config, command, mirror=None, as_root=False):
    if not os.path.exists(config["path"]):
        create(config, mirror)

    root = Root(config)

    root.activate()
    try:
        root.run(command, as_root=as_root)
    finally:
        root.deactivate()


def main():
    if not os.geteuid() == 0:
        sys.exit("You must run the command as root")

    os.environ["BROOT"] = "yes"

    with open("root.json") as f:
        config = json.load(f)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    shell_parser = subparsers.add_parser("shell")
    shell_parser.add_argument("--root", action="store_true")

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--mirror")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--mirror")
    run_parser.add_argument("--root", action="store_true")
    run_parser.add_argument("subcommand", nargs="+")

    subparsers.add_parser("update")
    subparsers.add_parser("clean")

    args = parser.parse_args()
    if args.command == "create":
        create(config, args.mirror)
    elif args.command == "run":
        run(config, " ".join(args.subcommand), args.mirror, as_root=args.root)
    elif args.command == "shell":
        run(config, "/bin/bash", as_root=args.root)
    elif args.command == "update":
        update(config)
    elif args.command == "clean":
        clean(config)

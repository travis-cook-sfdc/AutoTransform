# AutoTransform
# Large scale, component based code modification library
#
# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2022-present Nathan Rockenbach <http://github.com/nathro>

# @black_format

"""The schedule command is used to schedule runs of AutoTransform."""

import json
import time
from argparse import ArgumentParser, Namespace

from autotransform.event.debug import DebugEvent
from autotransform.event.handler import EventHandler
from autotransform.event.logginglevel import LoggingLevel
from autotransform.event.run import ScriptRunEvent
from autotransform.util.schedule import Schedule


def add_args(parser: ArgumentParser) -> None:
    """Adds the args to a subparser that are required to schedule runs.

    Args:
        parser (ArgumentParser): The parser for the schedule command.
    """

    parser.add_argument(
        "schedule",
        metavar="schedule",
        type=str,
        help="A file path to the JSON encoded schedule of schema runs to execute.",
    )
    parser.add_argument(
        "-t",
        "--time",
        metavar="time",
        type=int,
        required=False,
        help="The timestamp to use in place of the current time, used in cases where delays in "
        + "scheduling are likely.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        required=False,
        help="Tells the script to output verbose logs.",
    )
    parser.set_defaults(func=schedule_command_main)


def schedule_command_main(args: Namespace) -> None:
    """The main method for the schedule command, handles the actual execution of scheduling runs.

    Args:
        args (Namespace): The arguments supplied to the schedule command, such as the JSON file.
    """

    # pylint: disable=unspecified-encoding

    start_time = int(args.time) if args.time is not None else int(time.time())
    event_handler = EventHandler.get()
    if args.verbose:
        event_handler.set_logging_level(LoggingLevel.DEBUG)

    # Get Schedule Data
    schedule_file = args.schedule
    event_args = {"schedule_file": schedule_file}
    with open(schedule_file, "r") as file:
        schedule_json = file.read()
    event_args["schedule"] = schedule_json
    event_handler.handle(DebugEvent({"message": f"Schedule: ({args.schedule})\n{schedule_json}"}))
    schedule_data = json.loads(schedule_json)

    event_handler.handle(ScriptRunEvent({"script": "schedule", "args": event_args}))

    # Get needed info/objects for scheduling
    schedule = Schedule.from_data(schedule_data, start_time)
    event_handler.get().handle(DebugEvent({"message": f"Running schedule: {schedule}"}))
    schedule.run(start_time)

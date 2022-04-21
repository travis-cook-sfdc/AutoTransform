# AutoTransform
# Large scale, component based code modification library
#
# Licensed under the MIT License <http://opensource.org/licenses/MIT
# SPDX-License-Identifier: MIT
# Copyright (c) 2022-present Nathan Rockenbach <http://github.com/nathro>

"""An example module containing custom imports. Used via the custom_components config setting.
All custom component imports should follow this structure. Component types that do not have any
custom implementations do not need to be included (i.e. if there are no custom batchers, the
BATCHERS variable can be left out."""

from typing import Any, Callable, Dict, List, Mapping, Type

from autotransform.batcher.base import Batcher
from autotransform.command.base import Command
from autotransform.event.base import Event
from autotransform.filter.base import Filter
from autotransform.input.base import Input
from autotransform.runner.base import Runner
from autotransform.schema.builder import SchemaBuilder
from autotransform.transformer.base import Transformer
from autotransform.validator.base import Validator

# See autotransform.batcher.factory
BATCHERS: Dict[str, Callable[[Mapping[str, Any]], Batcher]] = {}
# See autotransform.command.factory
COMMANDS: Dict[str, Callable[[Mapping[str, Any]], Command]] = {}
# See autotransform.event.handler
EVENT_CALLBACKS: List[Callable[[Event], None]] = []
# See autotransform.filter.factory
FILTERS: Dict[str, Callable[[bool, Mapping[str, Any]], Filter]] = {}
# See autotransform.input.factory
INPUTS: Dict[str, Callable[[Mapping[str, Any]], Input]] = {}
# See autotransform.runner.factory
RUNNERS: Dict[str, Callable[[Mapping[str, Any]], Runner]] = {}
# See autotransform.schema.builder
SCHEMAS: Dict[str, Type[SchemaBuilder]] = {}
# See autotransform.transformer.factory
TRANSFORMERS: Dict[str, Callable[[Mapping[str, Any]], Transformer]] = {}
# See autotransform.validator.factory
VALIDATORS: Dict[str, Callable[[Mapping[str, Any]], Validator]] = {}
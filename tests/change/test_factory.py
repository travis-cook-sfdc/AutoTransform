# AutoTransform
# Large scale, component based code modification library
#
# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2022-present Nathan Rockenbach <http://github.com/nathro>

# @black_format

"""Tests that the Change's factory is correctly setup."""

import json
from typing import Dict, List

from autotransform.change.base import FACTORY, Change, ChangeName
from autotransform.change.github import GithubChange


def test_all_enum_values_present():
    """Ensures that all values from the enum are present in the factory map,
    and only enum values are present."""

    missing_values = [
        change_type for change_type in ChangeName if change_type not in FACTORY.get_components()
    ]
    assert not missing_values, "Types missing from factory: " + ", ".join(missing_values)

    extra_values = [
        change_type for change_type in FACTORY.get_components() if change_type not in ChangeName
    ]
    assert not extra_values, "Extra types in factory: " + ", ".join(extra_values)


def test_fetching_components():
    """Ensures that all components can be fetched correctly."""

    for component_type in FACTORY.get_components():
        component_class = FACTORY.get_class(component_type)
        assert (
            component_class.name == component_type
        ), f"Component {component_type} has wrong type {component_class.name}"

    for component_type in FACTORY.get_custom_components(strict=True):
        component_class = FACTORY.get_class(component_type)
        assert (
            f"custom/{component_class.name}" == component_type
        ), f"Component {component_type} has wrong type {component_class.name}"


def test_encoding_and_decoding():
    """Tests the encoding and decoding of components."""

    test_components: Dict[ChangeName, List[Change]] = {
        ChangeName.GITHUB: [
            GithubChange(full_github_name="nathro/ATTest", pull_number=1),
        ],
    }

    for name in ChangeName:
        assert name in test_components, f"No test components for Change {name}"

    for name, components in test_components.items():
        assert name in ChangeName, f"{name} is not a valid ChangeName"
        for component in components:
            assert (
                component.name == name
            ), f"Testing change of type {component.name} for type {name}"
            assert (
                FACTORY.get_instance(json.loads(json.dumps(component.bundle()))) == component
            ), f"Component {component} does not bundle and unbundle correctly"

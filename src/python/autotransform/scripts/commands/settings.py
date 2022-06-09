# AutoTransform
# Large scale, component based code modification library
#
# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2022-present Nathan Rockenbach <http://github.com/nathro>

# @black_format

"""The settings command is used to update AutoTransform settings, such as scheduler.json files,
manager.json files, configs and imported components."""

import json
import os
from argparse import ArgumentParser, Namespace
from typing import Dict, List

from autotransform.config.config import Config
from autotransform.config.default import DefaultConfigFetcher
from autotransform.util.component import ComponentFactory, ComponentImport
from autotransform.util.console import choose_option_from_list, error, get_str, info
from autotransform.util.package import get_config_dir


def add_args(parser: ArgumentParser) -> None:
    """Adds the args to a subparser that are required to update/view settings.

    Args:
        parser (ArgumentParser): The parser for the command.
    """

    setting_type_group = parser.add_mutually_exclusive_group(required=True)
    setting_type_group.add_argument(
        "--user-config",
        dest="setting_type",
        action="store_const",
        const="user_config",
        help="Update or view the user configuration for AutoTransform",
    )
    setting_type_group.add_argument(
        "--repo-config",
        dest="setting_type",
        action="store_const",
        const="repo_config",
        help="Update or view the repo configuration for AutoTransform",
    )
    setting_type_group.add_argument(
        "--cwd-config",
        dest="setting_type",
        action="store_const",
        const="cwd_config",
        help="Update or view the current working directory configuration for AutoTransform",
    )
    setting_type_group.add_argument(
        "--custom_components",
        dest="setting_type",
        action="store_const",
        const="custom_components",
        help="Update or view custom components",
    )

    parser.add_argument(
        "--update",
        dest="update_settings",
        action="store_true",
        help="Used to indicate updates are to be made to the settings.",
    )

    parser.set_defaults(func=settings_command_main, update_settings=False)


def settings_command_main(args: Namespace) -> None:
    """The main method for the settings command, handles the actual execution of updating
    and viewing settings.

    Args:
        args (Namespace): The arguments supplied to the settings command.
    """

    if args.setting_type == "user_config":
        path = f"{get_config_dir}/{DefaultConfigFetcher.FILE_NAME}"
        handle_config(path, "User", args.update_settings)
    elif args.setting_type == "repo_config":
        path = f"{DefaultConfigFetcher.get_repo_config_dir()}/{DefaultConfigFetcher.FILE_NAME}"
        handle_config(path, "Repo", args.update_settings)
    elif args.setting_type == "cwd_config":
        path = f"{DefaultConfigFetcher.get_cwd_config_dir()}/{DefaultConfigFetcher.FILE_NAME}"
        handle_config(path, "CWD", args.update_settings)
    elif args.setting_type == "custom_components":
        handle_custom_components(args)


def handle_config(path: str, config_type: str, update: bool) -> None:
    """Handles updating a config file.

    Args:
        path (str): The path to the file.
        config_type (str): The type of config being updated (i.e. user).
        update (bool): Whether to update the config.
    """

    config = Config.read(path)
    info(f"Current {config_type} Config: {config!r}")
    if update:
        config.from_console(config, user_config=config_type == "User")[0].write(path)


def handle_custom_components(args: Namespace) -> None:
    """Handle updating/viewing custom components

    Args:
        args (Namespace): The arguments supplied to the settings command.
    """

    component_file_name = choose_option_from_list(
        "Select a component type:",
        [
            ("input.json", "Inputs"),
            ("filter.json", "Filters"),
            ("batcher.json", "Batchers"),
            ("transformer.json", "Transformers"),
            ("validator.json", "Validators"),
            ("repo.json", "Repos"),
            ("schema_builder.json", "Schema Builders"),
            ("runner.json", "Runners"),
            ("item.json", "Items"),
            ("change.json", "Changes"),
            ("step.json", "Steps"),
            ("condition.json", "Conditions"),
        ],
    )
    component_dict = ComponentFactory.get_custom_components_dict(component_file_name, strict=False)
    if component_dict:
        info("Custom components:")
        for name, component_import in component_dict.items():
            info(f"\t{name.removeprefix('custom/')}: {component_import!r}")
    else:
        info("No existing custom components")
    if args.update_settings:
        # Remove components
        components_to_remove = get_components_to_remove(component_dict)
        changed = bool(components_to_remove)
        for component in components_to_remove:
            del component_dict[component]

        # Add components
        components_to_add = get_components_to_add(component_dict)
        changed = changed or bool(components_to_add)
        component_dict = component_dict | components_to_add

        if changed:
            file_path = ComponentFactory.get_custom_components_path(component_file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w+", encoding="UTF-8") as component_file:
                component_file.write(
                    json.dumps(
                        {k.removeprefix("custom/"): v.bundle() for k, v in component_dict.items()},
                        indent=4,
                    )
                )
                component_file.flush()


def get_components_to_remove(component_dict: Dict[str, ComponentImport]) -> List[str]:
    """Gets a list of components to remove from the dictionary using console input.

    Args:
        component_dict (Dict[str, ComponentImport]): The custom component dictionary.

    Returns:
        List[str]: The keys to remove from the dictionary.
    """

    components = []
    if component_dict:
        name = get_str("Enter a component name to remove(blank to skip): ")
    else:
        name = ""
    while name != "":
        if name.startswith("custom/"):
            name = name.removeprefix("custom/")
        if f"custom/{name}" not in component_dict:
            error(f"No component import with name: {name}")
        elif f"custom/{name}" in components:
            error(f"Already removing component import with name: {name}")
        else:
            components.append(f"custom/{name}")
        if len(component_dict) <= len(components):
            break
        name = get_str("Enter a component name to remove(blank to skip): ")
    return components


def get_components_to_add(component_dict: Dict[str, ComponentImport]) -> Dict[str, ComponentImport]:
    """Gets a dictionary of new components to add to the custom component imports.

    Args:
        component_dict (Dict[str, ComponentImport]): The existing custom components.

    Returns:
        Dict[str, ComponentImport]: The components to add to the dictionary.
    """

    components_to_add = {}
    name = get_str("Enter component name to add(blank to skip): ")
    while name != "":
        if name.startswith("custom/"):
            name = name.removeprefix("custom/")
        if f"custom/{name}" in component_dict:
            error(f"Component already exists with name: {name}")
        elif f"custom/{name}" in components_to_add:
            error(f"Already adding component with name: {name}")
        else:
            class_name = get_str("Enter the class representing this component: ")
            module = get_str("Enter the fully qualified name of the module for the class: ")
            components_to_add[f"custom/{name}"] = ComponentImport(
                class_name=class_name, module=module
            )
        name = get_str("Enter component name to add(blank to skip): ")

    return components_to_add

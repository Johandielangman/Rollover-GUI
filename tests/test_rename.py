import pytest
import os
import pathlib

import utils
from gui.structures import Registry
import shutil


ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
backup_path = pathlib.Path(os.path.join(ROOT_DIR, "backup"))
input_path = pathlib.Path(os.path.join(ROOT_DIR, "input"))
output_path = pathlib.Path(os.path.join(ROOT_DIR, "output"))

# delete input folder and copy over backup files
if input_path.exists():
    for f in input_path.iterdir():
        f.unlink()
else:
    input_path.mkdir()

for f in backup_path.iterdir():
    shutil.copy(f, input_path / f.name)

if output_path.exists():
    for f in output_path.iterdir():
        f.unlink()
else:
    output_path.mkdir()


def check_output_file_exists(registry: Registry):
    for _, to_name in registry.rename_mapping.items():
        to_path = pathlib.Path(os.path.join(registry.output_folder_root, to_name))
        assert to_path.exists()


@pytest.mark.parametrize(
    "input_file, expected_output",
    [
        pytest.param("important_work_2024.xlsx", "important_work_2025.xlsx", id="year separate"),
        pytest.param("important_work_2024_2023.xlsx", "important_work__ (2025).xlsx", id="two years"),
        pytest.param("report2024.xlsx", "report2025.xlsx", id="year combined"),
        pytest.param("report12345.xlsx", "report12345 (2025).xlsx", id="year not found"),
        pytest.param("report1234.xlsx", "report1234 (2025).xlsx", id="4 digit, not a year")
    ]
)
def test_rename_year(input_file, expected_output):
    registry: Registry = Registry(
        input_folder_root=str(input_path.absolute()),
        output_folder_root=str(output_path.absolute()),
        selected_files={
            input_file: True,
        },
        selected_suffix=" (my suffix)",
        selected_year="2025",
        use_year=True,
        use_suffix=False
    )
    utils.Rename(
        registry=registry
    )
    assert registry.rename_mapping[input_file] == expected_output

    utils.apply_rename_to_registry(registry)
    check_output_file_exists(registry)


@pytest.mark.parametrize(
    "input_file, expected_output",
    [
        pytest.param("important_work_2024.xlsx", "important_work_2024 (my suffix).xlsx", id="year separate"),
        pytest.param("important_work_2024_2023.xlsx", "important_work_2024_2023 (my suffix).xlsx", id="two years"),
        pytest.param("report2024.xlsx", "report2024 (my suffix).xlsx", id="year combined"),
        pytest.param("report12345.xlsx", "report12345 (my suffix).xlsx", id="year not found"),
        pytest.param("report1234.xlsx", "report1234 (my suffix).xlsx", id="4 digit, not a year")
    ]
)
def test_suffix(input_file, expected_output):
    registry: Registry = Registry(
        input_folder_root=str(input_path.absolute()),
        output_folder_root=str(output_path.absolute()),
        selected_files={
            input_file: True,
        },
        selected_suffix=" (my suffix)",
        selected_year="2025",
        use_year=False,
        use_suffix=True
    )
    utils.Rename(
        registry=registry
    )
    assert registry.rename_mapping[input_file] == expected_output

    utils.apply_rename_to_registry(registry)
    check_output_file_exists(registry)


@pytest.mark.parametrize(
    "input_file, expected_output",
    [
        pytest.param("important_work_2024.xlsx", "important_work_2025 (my suffix).xlsx", id="year separate"),
        pytest.param("important_work_2024_2023.xlsx", "important_work__ (2025) (my suffix).xlsx", id="two years"),
        pytest.param("report2024.xlsx", "report2025 (my suffix).xlsx", id="year combined"),
        pytest.param("report12345.xlsx", "report12345 (2025) (my suffix).xlsx", id="year not found"),
        pytest.param("report1234.xlsx", "report1234 (2025) (my suffix).xlsx", id="4 digit, not a year")
    ]
)
def test_rename_year_and_suffix(input_file, expected_output):
    registry: Registry = Registry(
        input_folder_root=str(input_path.absolute()),
        output_folder_root=str(output_path.absolute()),
        selected_files={
            input_file: True,
        },
        selected_suffix=" (my suffix)",
        selected_year="2025",
        use_year=True,
        use_suffix=True
    )
    utils.Rename(
        registry=registry
    )
    assert registry.rename_mapping[input_file] == expected_output

    utils.apply_rename_to_registry(registry)
    check_output_file_exists(registry)

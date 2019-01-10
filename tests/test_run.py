from unittest.mock import patch, sentinel, call

import pytest

from reformat_money.run import parse_args_and_reformat, reformatter


@patch("reformat_money.run.reformatter")
@patch("reformat_money.run.get_args")
def test_parse_args_and_reformat(mock_get_args, mock_reformatter):
    args = {"arg1": sentinel.arg1}
    mock_get_args.return_value = args
    parse_args_and_reformat()
    mock_get_args.assert_called_once_with()
    mock_reformatter.assert_called_once_with(arg1=sentinel.arg1)


def test_reformatter_raises_runtime_error_when_not_file_or_dir():
    with pytest.raises(RuntimeError) as exc_info:
        reformatter("foo")
    assert str(exc_info.value) == (
        "path provided is not a directory or file, or does not have the correct extension: foo"
    )


@patch("reformat_money.run.FileFormatter")
@patch("reformat_money.run.os.path.isfile", return_value=True)
def test_reformatter_with_single_file(mock_isfile, mock_file_formatter):
    file = "foo.py"
    reformatter(file)
    mock_file_formatter.assert_called_once_with(file)


@patch("reformat_money.run.FileFormatter")
@patch("reformat_money.run.get_files")
@patch("reformat_money.run.os.path.isfile", return_value=False)
@patch("reformat_money.run.os.path.isdir", return_value=True)
def test_reformatter_when_path_is_directory(mock_isdir, mock_isfile, mock_get_files, mock_file_formatter):
    file1 = "foo.py"
    file2 = "bar.py"
    mock_get_files.return_value = [file1, file2]
    reformatter("dirname")
    assert mock_file_formatter.call_count == 2
    assert mock_file_formatter.call_args_list == [
        call(file1),
        call(file2),
    ]


@patch("reformat_money.run.os.path.isfile", return_value=True)
def test_reformatter_with_single_file_does_not_match_extension(mock_isfile):
    file = "foo.c"
    with pytest.raises(RuntimeError) as exc_info:
        reformatter(file)
    assert str(exc_info.value) == (
        "path provided is not a directory or file, or does not have the correct extension: foo.c"
    )
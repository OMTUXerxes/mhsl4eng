"""Check the mechanical parts of a generated practice sheet."""

import argparse
import re
from pathlib import Path


ITEM = re.compile(r"^\s*(\d+)[.．、]\s*(\S.*)$")
SECTION = re.compile(r"^第[一二三四五六七八九十]+部分：")
WORD_GROUP = re.compile(r"^同类词(?:（[^）]+）)?：\s*(\S.*)$")


def validate(text: str, expected_count: int = 10, phonics: bool = False) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    errors = []
    markers = [
        "第一部分：老师讲解",
        "第二部分：专项练习",
        "基础题：",
        "进阶题：",
        "参考答案：",
    ]
    positions = []
    for marker in markers:
        matches = [i for i, line in enumerate(lines) if line.startswith(marker)]
        if len(matches) != 1:
            errors.append(f"“{marker}”应出现一次，实际出现 {len(matches)} 次")
        positions.append(matches[0] if matches else -1)

    if sum(bool(SECTION.match(line)) for line in lines) != 2:
        errors.append("正式输出必须恰好有两个部分")
    if any(pos < 0 for pos in positions):
        return errors
    if positions != sorted(positions) or len(set(positions)) != len(positions):
        errors.append("老师讲解、练习、基础题、进阶题、参考答案的顺序不正确")
        return errors

    teacher, exercises, basic, advanced, answers = positions
    if any(lines[:teacher]):
        errors.append("第一部分前有多余内容")
    if not any(lines[teacher + 1 : exercises]):
        errors.append("老师讲解为空")

    question_lines = lines[exercises + 1 : basic]
    answer_lines = lines[answers + 1 :]
    questions = [ITEM.match(line) for line in question_lines]
    questions = [match for match in questions if match]
    keys = [ITEM.match(line) for line in answer_lines]
    keys = [match for match in keys if match]
    expected = list(range(1, expected_count + 1))
    if [int(match.group(1)) for match in questions] != expected:
        errors.append(f"练习题应按 1 到 {expected_count} 连续编号")
    if [int(match.group(1)) for match in keys] != expected:
        errors.append(f"参考答案应按 1 到 {expected_count} 连续编号")
    if any(re.search(r"【\s*(?:基础|进阶)", match.group(2)) for match in questions):
        errors.append("不能在单题前标注基础或进阶")

    basic_numbers = [int(n) for n in re.findall(r"\d+", lines[basic])]
    advanced_numbers = [int(n) for n in re.findall(r"\d+", lines[advanced])]
    classified = basic_numbers + advanced_numbers
    if len(classified) != len(set(classified)) or sorted(classified) != expected:
        errors.append("基础题和进阶题的题号应各出现一次，并覆盖所有题目")
    if phonics:
        word_groups = [i for i, line in enumerate(lines) if WORD_GROUP.match(line)]
        if len(word_groups) != 1 or not advanced < word_groups[0] < answers:
            errors.append("音形对应练习应在难度题号后、参考答案前列出一行同类词")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="UTF-8 练习文本文件")
    parser.add_argument("--count", type=int, default=10, help="预期题数，默认 10")
    parser.add_argument("--phonics", action="store_true", help="检查音形对应练习是否列出同类词")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("--count 必须大于 0")
    try:
        content = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        parser.error(str(exc))
    problems = validate(content, args.count, args.phonics)
    if problems:
        for problem in problems:
            print(f"未通过：{problem}")
        return 1
    print(f"格式通过：{args.count} 道题及答案编号完整")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

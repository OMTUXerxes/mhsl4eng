# mhsl4eng

根据学生的英语错误生成简短讲解和针对性练习的 Codex Skill。支持文字错题、原题、学生答案及作业或试卷图片。默认生成 10 道题，并附基础/进阶题号与参考答案。

第一版使用 Skill 指令和大语言模型分析、出题，无需训练独立模型。

## 安装

把仓库克隆到 Codex 的 `skills` 目录，文件夹名保持为 `mhsl4eng`。

Windows PowerShell：

```powershell
$skillBase = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }
New-Item -ItemType Directory -Force -Path $skillBase | Out-Null
git clone https://github.com/OMTUXerxes/mhsl4eng.git (Join-Path $skillBase 'mhsl4eng')
```

安装后开启新的 Codex 对话，直接描述学生的错误，或输入 `$mhsl4eng` 显式调用。

## 使用示例

- `学生把 hope 拼成 hop，请出 10 道针对性练习。`
- `学生把 light 拼成 lait，我判断他没掌握 -ight 的读音。请给 l____ 这类拼写练习，并列出同类词。`
- `学生把 waste 拼成 wast，请给 w---- 这类练习，让他练 aste，并用 paste、haste 对照。`
- `学生写了 He like apples.，原句应为 He likes apples.，请出 5 道题。`
- `学生在这里漏写 the。请根据这张试卷照片出题。`

图片或原题不足以判断正确答案时，Skill 会先请你补充关键信息。详细规则见 [SKILL.md](SKILL.md)。

## 项目结构

- [SKILL.md](SKILL.md)：触发条件、执行流程和规则优先级。
- [references](references)：错误分类、错因判断、出题规则和输出规范。
- [scripts/validate_exercises.py](scripts/validate_exercises.py)：检查题数、编号、难度题号及两部分结构。
- [tests/test_cases.md](tests/test_cases.md)：不同错误类型和边界情况的测试案例。

校验生成的 UTF-8 文本：

```powershell
python scripts/validate_exercises.py exercise.txt --count 10
```

音形对应练习再加 `--phonics`，检查是否单独列出同类词。

脚本只检查能程序化判断的格式；错因、题目和答案仍需逐题核对。

## 许可

MIT，见 [LICENSE](LICENSE)。

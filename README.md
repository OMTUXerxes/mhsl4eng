# mhsl4eng

根据学生的英语错误生成简短讲解和针对性练习的 Codex Skill。支持文字错题、原题、学生答案及作业或试卷图片。默认生成 10 道题，并附基础/进阶题号与参考答案。

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
- `学生写了 He like apples.，原句应为 He likes apples.，请出 5 道题。`
- `学生在这里漏写 the。请根据这张试卷照片出题。`

图片或原题不足以判断正确答案时，Skill 会先请你补充关键信息。详细规则见 [SKILL.md](SKILL.md)。

## 许可

MIT，见 [LICENSE](LICENSE)。

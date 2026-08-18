<div align="center">

# Lightweight Project Skills

**面向使用 AI Agent 独立推进长期、多文件项目的轻量项目控制层。**

[English](README.md)

[![CI](https://github.com/KKLL2025/lightweight-project-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/KKLL2025/lightweight-project-skills/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/KKLL2025/lightweight-project-skills?include_prereleases&label=release)](https://github.com/KKLL2025/lightweight-project-skills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-4b3baf)](https://agentskills.io)

</div>

```bash
npx skills add KKLL2025/lightweight-project-skills
```

这个项目只从一条规则出发：普通选择交给模型判断，错了代价很高的事实必须验证。暂定想法不等于已批准范围，handoff 不能替代对相关项目实时状态的核实，目录看起来更整齐也不能证明迁移没有破坏项目。

仓库把这些失败面分给三个可组合 skill：**Align → Drive → Organize（对齐 → 推进 → 整理）。** 根据任务只用其中一个，或者按需组合。它们**不要求**每次修改都写 PRD、采用固定阶段文件、绑定某个 Issue 系统，或强制使用某种 shell、测试或委派方式。

> [!IMPORTANT]
> `0.6.0-preview` 是公开预览版。确定性工具已有测试，但行为证据仍主要来自小规模 Codex 试运行。关键项目使用前请在自己的模型和运行时中验证。

## 选择正确的 skill

| 情况 | 使用 | 负责内容 |
|---|---|---|
| 实质需求、关键决策、交付深度或可观察标准仍不清楚 | [`align-project-requirements`](skills/align-project-requirements/SKILL.md) | 用户真实需求、实质决策、假设、交付标准 |
| 执行需要跨多个有边界的批次、阶段、依赖或会话恢复 | [`drive-large-project`](skills/drive-large-project/SKILL.md) | 持续执行、可调整路线、活动状态、有边界的批次、可恢复 handoff |
| 项目树、文件放置、导航或被引用路径需要结构变化 | [`organize-ai-project-files`](skills/organize-ai-project-files/SKILL.md) | 目录拓扑、文件放置、导航、结构迁移 |
| 任务小、明确、可逆并能立即验证 | 直接执行 | 不需要新建管理文档 |

```text
实质目标不清楚 -> align-project-requirements
跨回合交付     -> drive-large-project
结构路径变化   -> organize-ai-project-files
明确的小任务   -> 直接执行
```

三个 skill 互相路由，但不重复维护同一事实。Align 负责需求基线和交付标准，Drive 负责可调整路线、活动状态、有边界的执行和可恢复 handoff，Organize 负责拓扑、放置和导航。handoff 是当前工作记忆，不是项目历史；文件夹名称也不能证明已经完成或正式发布。

在较长交付中，`drive-large-project` 会先选择一个有边界的执行批次。批次可以包含几个紧密相关的小步骤，也可以是困难里程碑中的一个连贯部分。当批次完成、实质受阻，或出现应由用户决定的问题时，它会保留已改变的状态，在有用时更新 handoff，简要汇报进展并结束本回合。里程碑用于组织项目路线，但不必与回合边界重合。只有现实出现理由时才重新检查已稳定的事实，而不是因为回合或会话发生变化就例行重查。

## 30 秒安装

### 一条命令（推荐）

安装了 Node.js 和 npm 后，使用开源的 [`skills` CLI](https://github.com/vercel-labs/skills)识别三个 skill，并选择目标 Agent 和安装范围：

```bash
npx skills add KKLL2025/lightweight-project-skills
```

如果要无交互地把三个 skill 全部复制到当前项目的 Codex 兼容目录：

```bash
npx skills add KKLL2025/lightweight-project-skills --skill '*' --agent codex --yes --copy
```

本仓库已经实际验证过远程识别，以及三个 skill 的 Codex 项目级复制安装。安装前仍应查看 skill 内容；安装后的 skill 会使用 Agent 本身拥有的权限。

### 手动安装备用方案

将 `skills/` 下需要的一个或全部文件夹复制到当前 Agent 运行时使用的 skills 目录。

### Windows PowerShell 下的 Codex

```powershell
$target = Join-Path $env:USERPROFILE '.codex\skills'
Copy-Item -Recurse -Force skills\align-project-requirements $target
Copy-Item -Recurse -Force skills\drive-large-project $target
Copy-Item -Recurse -Force skills\organize-ai-project-files $target
```

### POSIX 风格环境

```sh
mkdir -p ~/.codex/skills
cp -R skills/align-project-requirements ~/.codex/skills/
cp -R skills/drive-large-project ~/.codex/skills/
cp -R skills/organize-ai-project-files ~/.codex/skills/
```

安装后重启或刷新运行时。其他 Agent Skills 兼容运行时应使用其官方 skills 目录，不要直接套用 Codex 路径。

升级兼容说明：`v0.4.0-preview` 中的 `spec-workflow` 现名为 `align-project-requirements`。只应移除从本仓库安装的旧副本，不要影响其他提供方或插件中的旧同名 skill；同时启用本仓库的新旧副本可能造成重复触发。

## 使用示例

```text
使用 $align-project-requirements 对齐这个产品变更；如果没有实质决策阻塞，就继续实现。

使用 $drive-large-project 从项目真实状态恢复，完成下一个未阻塞结果。

使用 $organize-ai-project-files 整理项目根目录，不要破坏框架原生路径，也不要丢失用户资产。
```

更多触发、可复现场景和目录案例见 [examples](examples/README.md)。

## 文件夹治理

新建的 AI 主导或混合项目容器可以使用三分区主界面：

```text
project/
├── AGENTS.md
├── README.md
├── 01-ai-runtime/
├── 02-project-control/
└── 03-project-workspace/
```

成熟框架仓库采用兼容模式。`package.json`、`src/`、`app/`、CI 或 monorepo 清单等框架入口继续留在工具要求的位置。

GitHub 是可选的交付表面，不是三个 skill 的运行依赖。分支、提交、PR、外部授权和发布边界见 [GitHub 集成指南](docs/github-integration.md)。

## 验证

三个运行时 skill 不依赖第三方 Python 包。运行：

```sh
python -m unittest discover -s tests -v
```

CI 在 Windows/Linux 的 Python 3.11 和 3.13 上执行测试，覆盖 skill 合同、布局边界、纯移动/改名、重复内容、路径逃逸、符号链接策略、连续性与 handoff 卫生、中文路径、仓库链接和公开仓库卫生。

[`evals/cases.json`](evals/cases.json) 包含正例、反例和压力场景，并将原始提示与预期行为分离，便于进行不泄露答案的前向测试。

结构测试通过不等于所有模型都会遵守 skill。行为结论应同时保留原始提示、输出、模型/运行时身份、重复次数和无 skill 基线。

## 已验证与尚未验证

本预览版已验证：

- 三个 skill 通过本地结构校验；
- Python 单元测试在 Windows 本地通过；
- 对简单任务不干扰、陈旧 handoff 恢复、成熟仓库兼容布局和触发边界做过小规模 Codex 试运行；
- 运行时脚本只使用 Python 标准库。

尚未证明：

- 具有统计意义的跨模型行为提升；
- 在大量独立公开项目中的长期效果；
- 所有 Agent Skills 兼容运行时的完整安装验证；
- 生产级或安全认证。

稳定 `v1.0.0` 前需要的证据见 [ROADMAP.md](ROADMAP.md)。

## 设计参考

本项目吸收了 [Superpowers](https://github.com/obra/superpowers)、[GSD Core](https://github.com/open-gsd/gsd-core)、[CCPM](https://github.com/automazeio/ccpm) 和 [Agent Skills 规范](https://agentskills.io) 的工程与可发现性优点。核心差异是按风险治理：脆弱事实交给确定性工具，普通工作保留模型判断空间。

没有可复现证据时，本仓库不会发布“全面领先”或虚构评测徽章。

## 贡献与支持

- 修改 skill 或评测前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 普通问题使用 [GitHub Discussions](https://github.com/KKLL2025/lightweight-project-skills/discussions)。
- 可复现 Bug、聚焦的功能建议或脱敏后的真实项目案例使用 Issue 表单。
- 安全问题按 [SECURITY.md](SECURITY.md) 私密报告。

社区行为遵循 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)，版本变化记录在 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。所吸收上游工作的署名与许可证保留在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

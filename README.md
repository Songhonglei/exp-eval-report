# exp-eval-report

模型、Skill 与开源项目的实验和评测报告集合。

A collection of experiments and evaluation reports on models, skills, and open-source projects.

**[中文报告门户](https://songhonglei.github.io/exp-eval-report/) · [English report collection](https://songhonglei.github.io/exp-eval-report/en/)**

## 报告目录 Reports

| 编号 | 对象 | 中文报告 | 英文报告 | HuggingFace Report |
|---:|---|---|---|---|
| 1 | OrcaRouter 6-bit MLX | [OrcaRouter 本地拒答行为观察与评测方法反思](https://songhonglei.github.io/exp-eval-report/reports/orcarouter/zh/) | [Evaluating Refusal Behavior in OrcaRouter 6-bit MLX on Apple Silicon](https://songhonglei.github.io/exp-eval-report/reports/orcarouter/en/) | [Read](https://huggingface.co/datasets/EvanSong2008/orcarouter-6bit-mlx-evaluation-notes) |
| 2 | Qwen-Image 2.1 | [Mac M5 Pro 上 Qwen-Image 2.1 的本地部署与验证](https://songhonglei.github.io/exp-eval-report/reports/qwen-image-2-1/zh/) | [Running Qwen-Image 2.1 on a 48GB Mac M5 Pro](https://songhonglei.github.io/exp-eval-report/reports/qwen-image-2-1/en/) | [Read](https://huggingface.co/datasets/EvanSong2008/qwen-image-2-1-m5-pro-engineering-report) |

OrcaRouter 报告记录 114 个中文案例、160 次请求与评测协议缺陷；英文版是报告翻译，实验语言仍为中文。公开三份汇总 CSV，共 14 行数据，原始会话未公开。

Qwen-Image 报告记录 Q4/Q6 部署、MPS VAE 回环异常、992 方形编辑规避方案与 25 个后续生成任务。公开六份 API 工作流、九张关键原尺寸图像及任务摘要。

The OrcaRouter report covers 114 Chinese cases, 160 requests, and limitations of the evaluation protocol. Its English edition is a translation, not an English-language test. The Qwen-Image report covers deployment, VAE diagnostics, and Q4/Q6 observations. Each report retains its evidence scope, missing measurements, and AI-assistance disclosures.

## 多项目与多仓库来源 Multi-repo report collection

上游模型、Skill 和开源项目保留各自独立仓库。本仓库按项目归档报告，通过每份 `report.json` 记录来源、分类、语言、证据范围与跨平台链接，并生成统一报告门户。

Upstream projects retain their own repositories. Each report has a separate directory and manifest describing its sources, category, languages, evidence, and publication links. The portal is generated from those manifests.

```text
reports/
├── orcarouter/
│   ├── report.json
│   ├── ARTICLE.zh-CN.md / ARTICLE.en.md
│   ├── zh/ / en/                 # GitHub Pages editions
│   ├── assets/figures/
│   └── data/                     # Aggregate tables
└── qwen-image-2-1/
    ├── report.json
    ├── ARTICLE.zh-CN.md / ARTICLE.en.md
    ├── zh/ / en/
    ├── assets/figures/zh/ / en/
    └── evidence/                 # Workflows and selected evidence
assets/                           # Shared page design
scripts/                          # Static build and checks
templates/                        # New-report manifest template
```

分类使用 `models`、`skills`、`open-source`。目前已发布两份模型报告；后续可按同一结构加入 Skill 和开源项目实验。

## 构建与验证 Build and verify

构建只处理 Markdown、图片和元数据，不加载模型。GitHub Pages 使用 `main` 分支的根目录；生成的 HTML 一并提交，`.nojekyll` 保留静态路径。

The build processes local documents and metadata without model inference. Generated HTML is committed and served from the root of `main` by GitHub Pages.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/build_site.py
.venv/bin/python scripts/check_site.py
```

[新增报告指南 / Contributing](CONTRIBUTING.md) · [迁移说明 / Migration](MIGRATION.md)

## 引用与实验边界 Attribution and scope

各报告分别注明引用、模型版本、实验条件、AI 辅助过程与未完成的验证。迁移、翻译和发布不代表新增模型测试。第三方材料遵循各自的来源与许可；报告中出现模型或项目名称，不代表相应发布者认可本评测。

Each report documents its own sources and limitations. Migration, translation, and publication do not constitute new model experiments. Third-party material retains its original attribution and licensing; inclusion does not imply endorsement by an upstream publisher.

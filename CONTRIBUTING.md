# 新增实验报告 Adding a report

## 目录与来源

1. 在 `reports/<report-id>/` 创建独立目录，使用简短的 ASCII 标识。
2. 从 [manifest 模板](templates/report.json) 创建 `report.json`，填写真实分类、实验日期、上游来源、两种语言的标题和说明。
3. 保存 `ARTICLE.zh-CN.md` 与 `ARTICLE.en.md`。英文译稿应注明实际实验语言，保留缺失值、样本边界和方法缺陷。
4. 将公开图表放入 `assets/figures/`，把可公开的数据和工作流存入报告自己的 `data/` 或 `evidence/`。Markdown 的相对路径从本报告目录起算。
5. 填写 `source_repositories` 与 `huggingface` 链接，说明发布了哪些证据。只有实际公开的材料才能写为可下载。
6. 运行构建和检查，查看中英文桌面与移动页面，再将源文档和生成文件一起提交。

`category` 使用 `models`、`skills` 或 `open-source`。模板是结构示例，不会自动进入已发布报告目录。

## 证据与评测

正文应明确区分服务就绪、任务执行、任务完成与内容正确性。保留计时口径、样本选择方式、缺失测量和已知缺陷。发布前检查文件中没有凭据、个人绝对路径、未授权的私人材料或模型思考过程。第三方样本与材料需要保留来源和适用许可。

更新已有报告时，维护其原始实验日期和证据语义；新增实验使用新的记录，不把编辑工作描述为新的运行验证。若改名或移动目录，同步更新 Pages、Markdown 和 Hugging Face 的导航链接。

## Build workflow

Upstream projects remain separate repositories. Add one report directory per experiment, with a manifest, bilingual articles, figures, and explicitly scoped public evidence. Use `models`, `skills`, or `open-source` as the category.

```sh
.venv/bin/python scripts/build_site.py
.venv/bin/python scripts/check_site.py
```

The portal discovers `reports/*/report.json`. Do not place an incomplete template in that directory. The checker verifies local page links and anchors, language editions, the report registry, and the retained aggregate counts for the existing reports.

Keep factual claims tied to the actual experiment. Disclose translated editions and assisted annotations, preserve unavailable measurements, and distinguish observations from causal conclusions. Check desktop and mobile layouts before publishing.

# Companion evidence for Qwen Image 2.1 on a 48GB Mac

All results describe the October 20, 2026 local experiment. Preparing this package did not run models.

- [Environment and runtime arguments](environment.json)
- [Pinned model manifest](model-manifest.json)
- [Measurement definitions](measurement-method.json)
- [25-task summary with English domain labels](task-summary.csv)
- [Source task summary](task-summary.source.csv)
- [Original sensitive-prompt records](visual-cases.json)
- [English translations of visual observations](visual-observations.en.json)
- [VAE reconstruction metrics](vae-roundtrip.csv)
- [Static editorial verification](review-verification.json)
- [Original-size image index](image-evidence.json)

## Actual API graphs

The JSON files contain graph objects, not complete HTTP request bodies. Wrap a graph in the `prompt` field when submitting it to `/prompt`. They are not frontend canvas-format workflow exports.

| Task | Q4 | Q6 |
|---|---|---|
| 1024 text-to-image | [Q4 graph](workflows/qwen-image-2.1-Q4_K_M-t2i.api.json) | [Q6 graph](workflows/qwen-image-2.1-Q6_K-t2i.api.json) |
| 992 editing | [Q4 graph](workflows/qwen-image-2.1-Q4_K_M-image_edit.api.json) | [Q6 graph](workflows/qwen-image-2.1-Q6_K-image_edit.api.json) |

- [Failed 1024 Q4 edit](workflows/q4-edit-1024-failed.api.json), exported from the original saved PNG metadata.
- [VAE round trip](workflows/vae-roundtrip.api.json), exported from the original MPS BF16 diagnostic PNG. VAE device and precision are controlled by service arguments, not this graph alone; see the three recorded conditions in the article.

The [reference image](images/reference.png) preserves the decoded pixels of the experiment input. Check each graph's `LoadImage.inputs.image` and copy the reference into the ComfyUI input directory under that name, or adjust the input name explicitly. The figures are montages; use the original-size images for pixel calculations. PNG metadata was stripped without changing decoded pixel values.

## Scope of the bundle

There are nine selected teapot evidence images, not the complete set of 25 outputs. Model weights, virtual environments, credentials, personal absolute paths, and full raw logs are omitted. Model SHA-256 values report the completed download checks; editorial review did not reread the full weight files. Source inspection notes were assisted observations and are not independent human annotations.

# katsuo 🐟

[![Tests](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/AllBlue-inc/Katsuo/actions/workflows/test.yml)
![Live E2E](https://img.shields.io/badge/live%20E2E-Claude%20Code%20%2B%20Codex%20passed-2ea44f)
![Version](https://img.shields.io/badge/version-0.1.0-2563eb)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-d97757)
![Codex](https://img.shields.io/badge/Codex-plugin-111827)

[English](README.md) | **日本語**

Claude Code と Codex 用の開発プラグインです。仕様 → テスト駆動開発 → 独立レビュー → Pull Request の順に作業を進めます。

## インストール

**Claude Code**

```bash
claude plugin marketplace add AllBlue-inc/katsuo && claude plugin install katsuo@katsuo
```

**Codex**

```bash
codex plugin marketplace add AllBlue-inc/katsuo && codex plugin add katsuo@katsuo
```

Codexでは、インストール後に`/hooks`を開いてKatsuoのフックを信頼してください。

フックの実行には`PATH`上の`python3`が必要です。Pull Requestの作成には`gh` CLIを推奨します。

**更新:** `claude plugin marketplace update katsuo` · **削除:** `claude plugin uninstall katsuo@katsuo` / `codex plugin remove katsuo`

## 使い方

Claude Codeでは`/katsuo`、Codexでは`$katsuo`の後ろに、作りたいものを書きます。

```text
/katsuo メールによるパスワードリセットを追加
```

1. Katsuoが変更を Small か Big に分け、最初に作る機能を提案します。範囲に合意してください。
2. 初回だけ、プロジェクトについて質問されます（一度に最大3問、おすすめの回答つき）。答えると `docs/project.md` と `AGENTS.md` が作られます。
3. 仕様（`docs/specs/<名前>.md`）が示されるので、承認してください。
4. 実装とレビューが終わると、Pull Requestのリンクが届きます。マージはあなたが行います。

| ステップ | Katsuoがすること | あなたが決めること |
|---|---|---|
| 規模確認 | 変更を Small か Big に分け、最初に作る最小の機能を提案 | 取り組む範囲 |
| 初期設定（初回のみ） | プロジェクトを調べ、必要なことだけ質問し、ガードレールを設定 | 方針 |
| 仕様 | 受け入れ条件とタスクを作成 | 計画の承認 |
| 実装 | タスクごとにRed → Green → Refactor。試行は最大3回 | タスク単位または機能単位での承認 |
| レビュー | 読み取り専用のレビュアーが仕様、テスト、セキュリティ、シンプルさを確認 | 残った問題への対応 |
| PR | 機能ブランチをpushし、Pull Requestを作成 | マージするかどうか |

GitHubリポジトリでは、エージェントによる`main`/`master`へのpush、force-push、マージをフックで禁止しています。

## 方針

- 判断する前にプロジェクトを調べる。分からないことは推測で埋めない。
- 結果やリスクが変わる判断（プライバシー、セキュリティ、コスト、取り消せない操作）はユーザーに確認する。
- 作業を Small か Big に分け、役に立つ機能を一つずつ完成させる。
- 受け入れ条件に必要なものだけを作る。
- 専門用語をできるだけ使わずに説明する。

## 開発者向け

### 動作確認

```bash
python3 tests/e2e_smoke.py
python3 tests/e2e_smoke.py --live
```

- 1つ目は、パッケージの整合性と、マニフェストからフックまでの接続を確認します。Claude Code があればパッケージを検証し、Codex があれば Katsuo が有効かどうかも確認します。
- `--live`は、認証済みの Claude Code と Codex の両方で Katsuo を実行して応答を確認します。Claude はツールを無効にし、Codex は読み取り専用サンドボックスで動かします。認証情報はテストに保存しません。

2026-10-06に、両方のテストに合格しました。テストで確認できるのは上記の経路だけで、モデルが毎回同じ判断をすることまでは保証しません。

### ファイル構成

```text
skills/katsuo/SKILL.md  コマンドと作業手順
agents/reviewer.md      独立レビュアー（読み取り専用）
hooks/guard_git.py      Git操作のガード
tests/e2e_smoke.py      決定的テストとライブテスト
```

作者: Aakash
